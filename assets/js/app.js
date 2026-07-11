// Reemplazar por el número real en formato internacional, sin +, espacios ni guiones.
const WHATSAPP_PHONE = "5492477669952";

const EXCHANGE_PACK_SIZE = 7;

const EXCHANGE_RULE =
  `El canje se realiza tarjeta por tarjeta; si necesitás más tarjetas de las que vos me das; el canje se realiza 1 sobre cerrado cada ${EXCHANGE_PACK_SIZE} tarjetas.`;

const CLOSED_PACK_ONLY_RULE =
  `El cambio es de ${EXCHANGE_PACK_SIZE} tarjetas solicitadas por 1 sobre cerrado.`;

const state = {
  needed: new Map(),
  offered: new Map(),
  offeredHasStickers: true,
};

const elements = {
  loadStatus: document.querySelector("#load-status"),
  exchangeContent: document.querySelector("#exchange-content"),
  summary: document.querySelector("#summary"),
  formMessage: document.querySelector("#form-message"),
  exchangeRule: document.querySelector("#exchange-rule"),
  suggestedPacks: document.querySelector("#suggested-packs"),
  exchangeButton: document.querySelector("#exchange-button"),
  needed: {
    list: document.querySelector("#needed-list"),
    empty: document.querySelector("#needed-empty"),
    search: document.querySelector("#needed-search"),
    clear: document.querySelector("#needed-clear"),
    counter: document.querySelector("#needed-counter"),
    total: document.querySelector("#needed-total"),
  },
  offered: {
    tools: document.querySelector("#offered-tools"),
    list: document.querySelector("#offered-list"),
    empty: document.querySelector("#offered-empty"),
    search: document.querySelector("#offered-search"),
    clear: document.querySelector("#offered-clear"),
    counter: document.querySelector("#offered-counter"),
    total: document.querySelector("#offered-total"),
  },
  differenceTotal: document.querySelector("#difference-total"),
};

function normalizeDataset(dataset) {
  return Object.entries(dataset)
    .map(([country, cards]) => {
      const normalizedCards = cards
        .map((card, index) => normalizeCard(country, card, index))
        .filter(Boolean)
        .sort((a, b) => a.number - b.number || a.occurrence - b.occurrence);

      return [country.toUpperCase(), normalizedCards];
    })
    .filter(([, cards]) => cards.length > 0)
    .sort(([countryA], [countryB]) => countryA.localeCompare(countryB));
}

function deriveInventory(data) {
  if (!data.checklist || !data.stock) {
    return {
      repetidas: data.repetidas,
      faltantes: data.faltantes,
    };
  }

  const checklistByGroup = data.checklist;
  const stockQuantities = new Map();
  Object.values(data.stock).forEach((cards) => {
    if (!Array.isArray(cards)) {
      return;
    }
    cards.forEach((entry) => {
      const number = Number(entry?.number);
      const quantity = Number(entry?.quantity);
      if (Number.isInteger(number) && Number.isInteger(quantity)) {
        stockQuantities.set(number, quantity);
      }
    });
  });

  const repetidas = {};
  const faltantes = {};
  Object.entries(checklistByGroup).forEach(([group, cards]) => {
    repetidas[group] = [];
    faltantes[group] = [];
    if (!Array.isArray(cards)) {
      return;
    }

    cards.forEach((card) => {
      const quantity = stockQuantities.get(Number(card.number)) ?? 0;
      if (quantity <= 0) {
        faltantes[group].push({ ...card });
      } else if (quantity > 1) {
        repetidas[group].push({ ...card });
      }
    });
  });

  return { repetidas, faltantes };
}

function normalizeCard(country, card, occurrence) {
  if (!card || typeof card !== "object") {
    return null;
  }

  const number = Number(card.number);
  if (!Number.isFinite(number)) {
    return null;
  }

  return {
    country: country.toUpperCase(),
    number,
    name: typeof card.name === "string" ? card.name : "",
    position: card.position ?? null,
    occurrence,
  };
}

function itemKey(country, card) {
  return `${country}:${card.number}:${card.occurrence}`;
}

function createStickerOption(section, country, card) {
  const label = document.createElement("label");
  label.className = "sticker-option";

  const input = document.createElement("input");
  input.type = "checkbox";
  input.value = String(card.number);
  input.dataset.country = country;
  input.dataset.name = card.name;
  input.setAttribute("aria-label", `${country} tarjeta ${card.number} ${card.name}`);
  input.addEventListener("change", () => {
    const selection = state[section];
    const key = itemKey(country, card);

    if (input.checked) {
      selection.set(key, {
        country,
        number: card.number,
        name: card.name,
        occurrence: card.occurrence,
      });
    } else {
      selection.delete(key);
    }

    updateSummary();
  });

  const visibleNumber = document.createElement("span");
  visibleNumber.className = "sticker-number";
  visibleNumber.textContent = card.number;

  const visibleName = document.createElement("span");
  visibleName.className = "sticker-name";
  visibleName.textContent = card.name || "Sin nombre";

  label.title = card.name ? `${card.number} - ${card.name}` : String(card.number);
  label.append(input, visibleNumber, visibleName);
  return label;
}

function renderSection(section, dataset) {
  const fragment = document.createDocumentFragment();

  dataset.forEach(([country, cards]) => {
    const group = document.createElement("article");
    group.className = "country-group";
    group.dataset.country = country;
    group.dataset.numbers = cards
      .map((card) => `${card.number} ${card.name}`)
      .join(" ")
      .toUpperCase();

    const heading = document.createElement("h3");
    heading.className = "country-code";
    heading.textContent = country;

    const stickerGrid = document.createElement("div");
    stickerGrid.className = "sticker-grid";
    cards.forEach((card) => {
      stickerGrid.append(createStickerOption(section, country, card));
    });

    group.append(heading, stickerGrid);
    fragment.append(group);
  });

  elements[section].list.replaceChildren(fragment);

  if (section === "offered" && dataset.length === 0) {
    state.offeredHasStickers = false;
    elements.offered.tools.hidden = true;
    elements.offered.empty.className = "status status-warning";
    elements.offered.empty.textContent = CLOSED_PACK_ONLY_RULE;
    elements.offered.empty.hidden = false;
    elements.offered.search.disabled = true;
    elements.offered.clear.disabled = true;
  }
}

function filterSection(section) {
  if (section === "offered" && !state.offeredHasStickers) {
    elements.offered.empty.hidden = false;
    return;
  }

  const query = elements[section].search.value.trim().toUpperCase();
  let visibleGroups = 0;

  elements[section].list.querySelectorAll(".country-group").forEach((group) => {
    const countryMatches = group.dataset.country.includes(query);
    const cardMatches = group.dataset.numbers.includes(query);
    const isVisible = !query || countryMatches || cardMatches;

    group.hidden = !isVisible;
    visibleGroups += Number(isVisible);
  });

  elements[section].empty.hidden = visibleGroups > 0;
}

function clearSelection(section) {
  state[section].clear();
  elements[section].list.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
    checkbox.checked = false;
  });
  updateSummary();
}

function selectionByCountry(selection) {
  const grouped = new Map();

  [...selection.values()]
    .sort((a, b) => a.country.localeCompare(b.country) || a.number - b.number)
    .forEach(({ country, number, name }) => {
      if (!grouped.has(country)) {
        grouped.set(country, []);
      }
      grouped.get(country).push(name ? `${number} - ${name}` : String(number));
    });

  return grouped;
}

function formatSelection(selection) {
  return [...selectionByCountry(selection)]
    .map(([country, numbers]) => `${country}: ${numbers.join(", ")}`)
    .join("\n");
}

function updateSummary() {
  const neededTotal = state.needed.size;
  const offeredTotal = state.offered.size;
  const difference = Math.max(neededTotal - offeredTotal, 0);

  elements.needed.counter.textContent = `${neededTotal} seleccionada${neededTotal === 1 ? "" : "s"}`;
  elements.offered.counter.textContent = `${offeredTotal} seleccionada${offeredTotal === 1 ? "" : "s"}`;
  elements.needed.total.textContent = neededTotal;
  elements.offered.total.textContent = offeredTotal;
  elements.differenceTotal.textContent = difference;

  const ruleApplies = neededTotal > offeredTotal;
  elements.exchangeRule.hidden = !ruleApplies;
  if (ruleApplies) {
    const suggestedPacks = Math.ceil(difference / EXCHANGE_PACK_SIZE);
    elements.suggestedPacks.textContent =
      `Diferencia: ${difference} tarjeta${difference === 1 ? "" : "s"}. ` +
      `Sobres sugeridos: ${suggestedPacks}.`;
  }

  hideFormMessage();
}

function showFormMessage(message, type) {
  elements.formMessage.textContent = message;
  elements.formMessage.className = `status status-${type}`;
  elements.formMessage.hidden = false;
}

function hideFormMessage() {
  elements.formMessage.hidden = true;
  elements.formMessage.textContent = "";
}

function setSearchMode(isSearching) {
  elements.summary.classList.toggle("is-searching", isSearching);
}

function handleSearchBlur() {
  requestAnimationFrame(() => {
    const activeElement = document.activeElement;
    const searchInputs = [elements.needed.search, elements.offered.search];

    setSearchMode(searchInputs.includes(activeElement));
  });
}

function buildWhatsAppMessage() {
  const neededTotal = state.needed.size;
  const offeredTotal = state.offered.size;
  const difference = neededTotal - offeredTotal;
  const parts = [
    "Hola, quiero hacer un intercambio de tarjetas Adrenalyn XL FIFA 2026.",
    "",
    "Tarjetas que necesito:",
    formatSelection(state.needed),
    `Total que necesito: ${neededTotal}`,
    "",
    "Tarjetas que te doy:",
    offeredTotal > 0 ? formatSelection(state.offered) : "Ninguna seleccionada",
    `Total que te doy: ${offeredTotal}`,
  ];

  if (difference > 0) {
    parts.push(
      "",
      EXCHANGE_RULE,
      `Diferencia: ${difference} tarjeta${difference === 1 ? "" : "s"}.`,
      `Sobres sugeridos: ${Math.ceil(difference / EXCHANGE_PACK_SIZE)}.`,
    );
  }

  return parts.join("\n");
}

function startExchange() {
  if (state.needed.size === 0) {
    showFormMessage("Seleccioná al menos una tarjeta que necesitás.", "error");
    elements.formMessage.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  if (state.offered.size === 0) {
    showFormMessage(
      state.offeredHasStickers
        ? "No seleccionaste tarjetas para dar a cambio."
        : CLOSED_PACK_ONLY_RULE,
      "warning",
    );
  } else {
    hideFormMessage();
  }

  const url = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(buildWhatsAppMessage())}`;
  window.open(url, "_blank", "noopener,noreferrer");
}

async function loadData() {
  try {
    const dataUrl = new URL("data/figuritas.json", document.baseURI);
    dataUrl.searchParams.set("v", Date.now().toString());

    const response = await fetch(dataUrl, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`No se pudo cargar el JSON (${response.status}).`);
    }

    const data = await response.json();
    const inventory = deriveInventory(data);
    if (!inventory.repetidas || !inventory.faltantes) {
      throw new Error("El JSON no contiene stock/checklist ni repetidas/faltantes.");
    }

    const neededDataset = normalizeDataset(inventory.repetidas);
    const offeredDataset = normalizeDataset(inventory.faltantes);

    renderSection("needed", neededDataset);
    renderSection("offered", offeredDataset);
    elements.loadStatus.hidden = true;
    elements.exchangeContent.hidden = false;
    elements.summary.hidden = false;
    updateSummary();
  } catch (error) {
    elements.loadStatus.className = "status status-error";
    elements.loadStatus.textContent =
      "No se pudieron cargar las tarjetas. Abrí el sitio desde un servidor local o GitHub Pages.";
    console.error(error);
  }
}

elements.needed.search.addEventListener("input", () => filterSection("needed"));
elements.offered.search.addEventListener("input", () => filterSection("offered"));
elements.needed.search.addEventListener("focus", () => setSearchMode(true));
elements.offered.search.addEventListener("focus", () => setSearchMode(true));
elements.needed.search.addEventListener("blur", handleSearchBlur);
elements.offered.search.addEventListener("blur", handleSearchBlur);
elements.needed.clear.addEventListener("click", () => clearSelection("needed"));
elements.offered.clear.addEventListener("click", () => clearSelection("offered"));
elements.exchangeButton.addEventListener("click", startExchange);

loadData();
