const dimensions = ["appearance", "interior", "space", "intelligence", "driving", "range", "value"];

const i18n = {
  en: {
    brandName: "PM Decision OS",
    brandMeta: "New Energy Vehicle",
    navOverview: "Overview",
    navPortfolio: "Portfolio",
    navPriorities: "Priorities",
    navEvidence: "Evidence",
    navRecords: "Records",
    signalTitle: "Current Signal",
    workspace: "Product Management Dashboard",
    headline: "NEV Product IPA Decision Board",
    themeLabel: "Dark mode",
    themeLight: "Light mode",
    langLabel: "中文",
    filterBrand: "Brand",
    filterSeries: "Series",
    filterDimension: "Dimension",
    metricSamples: "Sample count",
    metricImportance: "Avg. importance",
    metricPerformance: "Avg. satisfaction",
    metricGap: "Max gap",
    portfolioEyebrow: "IPA Portfolio",
    portfolioTitle: "Original sample count, importance, and satisfaction",
    radarEyebrow: "Dimension View",
    radarTitle: "Importance and satisfaction",
    priorityEyebrow: "Roadmap Priorities",
    priorityTitle: "Highest importance-satisfaction gaps",
    matrixEyebrow: "IPA Matrix",
    matrixTitle: "Importance vs. satisfaction",
    evidenceEyebrow: "Comment Evidence",
    evidenceTitle: "User review snippets behind the selected dimension",
    truthEyebrow: "Data Lineage",
    truthTitle: "Is the IPA data real?",
    recordsEyebrow: "Series Records",
    recordsTitle: "Filtered rows from the original IPA matrix",
    decisionEyebrow: "PM Brief",
    decisionTitle: "Recommended action",
    allBrands: "All brands",
    allSeries: "All series",
    allDimensions: "All dimensions",
    brands: "brands",
    series: "series",
    samples: "samples",
    avgImportance: "Avg importance",
    avgSatisfaction: "Avg satisfaction",
    gap: "Gap",
    sourceImportance: "Weighted average of original importance scores",
    sourcePerformance: "Weighted average of original satisfaction scores",
    largestDimensionGap: "Largest dimension gap",
    improve: "Improve",
    maintain: "Maintain",
    monitor: "Monitor",
    filteredStatus: "source rows",
    importanceLine: "Importance line",
    satisfactionLine: "Satisfaction line",
    importanceMeaning: "Importance means how often and how strongly users mention this dimension in reviews or satisfaction/dissatisfaction fields.",
    satisfactionMeaning: "Satisfaction means the performance score for this dimension, calculated from user ratings and review sentiment in the offline IPA pipeline.",
    signalHeadline: "Interior has the largest gap: high importance, lower satisfaction.",
    signalMeta: "Use comments below to verify whether this is a real product pain point.",
    briefTitle: "Start with the largest verified gap, then read the comments.",
    briefBody: "The ranking comes from the original IPA matrix. The comment snippets are supporting evidence from processed UGC, not new metrics.",
    action1: "Check whether the high-gap dimension is repeated across several brands or only one series.",
    action2: "Use the original review text to separate product defects from expectation-management issues.",
    action3: "Treat low-sample series carefully before changing roadmap priority.",
    evidenceStatus: "UGC snippets",
    noEvidence: "No matching review snippet in the local evidence sample.",
    truthBody: "Yes, as processed analysis data. The IPA matrix is copied from offline-pipeline/data/Analyzed/IPA/step1_scores_matrix.csv and contains 110 series rows. It is not live market data; it is the result of the repository's offline pipeline.",
    truthPoint1: "Importance is computed from whether reviews mention each dimension and whether it appears in most/least satisfied text.",
    truthPoint2: "Satisfaction is computed from dimension ratings and review sentiment in the IPA scoring script.",
    truthPoint3: "This dashboard does not invent scores; it only aggregates, filters, and visualizes those original fields.",
    dimensions: {
      appearance: "Appearance",
      interior: "Interior",
      space: "Space",
      intelligence: "Intelligence",
      driving: "Driving",
      range: "Range",
      value: "Value"
    }
  },
  zh: {
    brandName: "产品决策 OS",
    brandMeta: "新能源汽车",
    navOverview: "总览",
    navPortfolio: "产品组合",
    navPriorities: "优先级",
    navEvidence: "评论证据",
    navRecords: "原始记录",
    signalTitle: "当前信号",
    workspace: "产品管理数据面板",
    headline: "新能源汽车 IPA 产品决策面板",
    themeLabel: "深色模式",
    themeLight: "浅色模式",
    langLabel: "EN",
    filterBrand: "品牌",
    filterSeries: "车系",
    filterDimension: "维度",
    metricSamples: "样本量",
    metricImportance: "平均重要度",
    metricPerformance: "平均满意度",
    metricGap: "最大差值",
    portfolioEyebrow: "IPA 产品组合",
    portfolioTitle: "原始样本量、重要度与满意度",
    radarEyebrow: "维度视图",
    radarTitle: "重要度与满意度",
    priorityEyebrow: "路线图优先级",
    priorityTitle: "重要度-满意度差值最高的维度",
    matrixEyebrow: "IPA 矩阵",
    matrixTitle: "重要度与满意度",
    evidenceEyebrow: "评论证据",
    evidenceTitle: "所选维度背后的用户评论片段",
    truthEyebrow: "数据链路",
    truthTitle: "IPA 数据是真的吗？",
    recordsEyebrow: "车系记录",
    recordsTitle: "来自原始 IPA 矩阵的筛选行",
    decisionEyebrow: "PM 简报",
    decisionTitle: "建议动作",
    allBrands: "全部品牌",
    allSeries: "全部车系",
    allDimensions: "全部维度",
    brands: "个品牌",
    series: "个车系",
    samples: "样本",
    avgImportance: "平均重要度",
    avgSatisfaction: "平均满意度",
    gap: "差值",
    sourceImportance: "原始重要度分数的样本加权平均",
    sourcePerformance: "原始满意度分数的样本加权平均",
    largestDimensionGap: "最大维度差值",
    improve: "重点改进",
    maintain: "保持优势",
    monitor: "持续观察",
    filteredStatus: "条原始行",
    importanceLine: "重要度线",
    satisfactionLine: "满意度线",
    importanceMeaning: "重要度表示用户在评论、最满意、最不满意文本中提到该维度的频率和强度。",
    satisfactionMeaning: "满意度表示该维度的表现分数，由离线 IPA 流程中的用户评分和评论情感计算得到。",
    signalHeadline: "内饰是当前最大差值：重要度高，但满意度明显落后。",
    signalMeta: "先看下方评论证据，判断它是产品痛点还是预期管理问题。",
    briefTitle: "先处理被评论证据支撑的最大差值。",
    briefBody: "排序来自原始 IPA 矩阵。评论片段来自已处理 UGC，只作为证据链，不新增指标。",
    action1: "确认高差值维度是跨品牌重复出现，还是集中在少数车系。",
    action2: "回看原始评论文本，区分产品缺陷与用户预期管理问题。",
    action3: "样本量较低的车系不要直接推动路线图优先级变化。",
    evidenceStatus: "UGC 片段",
    noEvidence: "本地证据样本中没有匹配的评论片段。",
    truthBody: "是真的，但它是处理后的分析数据。IPA 矩阵复制自 offline-pipeline/data/Analyzed/IPA/step1_scores_matrix.csv，包含 110 条车系记录。它不是实时市场数据，而是本项目离线流程的计算结果。",
    truthPoint1: "重要度来自评论是否提及该维度，以及该维度是否出现在最满意/最不满意文本中。",
    truthPoint2: "满意度来自维度评分和评论情感，由 IPA 评分脚本计算。",
    truthPoint3: "本面板不创造新分数，只做原始字段的聚合、筛选和可视化。",
    dimensions: {
      appearance: "外观",
      interior: "内饰",
      space: "空间",
      intelligence: "智能化",
      driving: "驾驶",
      range: "续航",
      value: "性价比"
    }
  }
};

const state = { lang: "en", theme: "light", brand: "all", series: "all", dimension: "all" };
let rows = [];
let evidenceRows = [];

const $ = (selector) => document.querySelector(selector);
const t = (key) => i18n[state.lang][key];
const dimensionLabel = (key) => i18n[state.lang].dimensions[key];

function normalizeRows(sourceRows) {
  return sourceRows.map((source) => {
    const row = { ...source };
    dimensions.forEach((dimension) => {
      row[`I_${dimension}`] = Number(row[`I_${dimension}`]);
      row[`P_${dimension}`] = Number(row[`P_${dimension}`]);
    });
    row.sample_count = Number(row.sample_count);
    return row;
  });
}

function formatCount(value) {
  return value >= 1000 ? `${(value / 1000).toFixed(1)}k` : String(value);
}

function score(value) {
  return (value * 100).toFixed(1);
}

function filteredRows() {
  return rows.filter((row) => {
    const brandMatch = state.brand === "all" || row.brand === state.brand;
    const seriesMatch = state.series === "all" || row.series === state.series;
    return brandMatch && seriesMatch;
  });
}

function weightedAverage(items, getter) {
  const total = items.reduce((sum, item) => sum + item.sample_count, 0);
  if (!total) return 0;
  return items.reduce((sum, item) => sum + getter(item) * item.sample_count, 0) / total;
}

function rowAverage(row, prefix) {
  return dimensions.reduce((sum, dimension) => sum + row[`${prefix}_${dimension}`], 0) / dimensions.length;
}

function dimensionStats(items) {
  return dimensions.map((dimension) => {
    const importance = weightedAverage(items, (row) => row[`I_${dimension}`]);
    const satisfaction = weightedAverage(items, (row) => row[`P_${dimension}`]);
    return { dimension, importance, satisfaction, gap: importance - satisfaction };
  });
}

function selectedStats(items) {
  const stats = dimensionStats(items);
  return state.dimension === "all" ? stats : stats.filter((item) => item.dimension === state.dimension);
}

function topGap(items) {
  return [...selectedStats(items)].sort((a, b) => b.gap - a.gap)[0] || dimensionStats(items)[0];
}

function aggregateByBrand(items) {
  const groups = new Map();
  items.forEach((row) => {
    if (!groups.has(row.brand)) groups.set(row.brand, []);
    groups.get(row.brand).push(row);
  });
  return [...groups.entries()].map(([brand, group]) => {
    const stats = state.dimension === "all" ? dimensionStats(group) : selectedStats(group);
    return {
      brand,
      series: group.length,
      sample_count: group.reduce((sum, row) => sum + row.sample_count, 0),
      avgImportance: state.dimension === "all" ? weightedAverage(group, (row) => rowAverage(row, "I")) : weightedAverage(group, (row) => row[`I_${state.dimension}`]),
      avgSatisfaction: state.dimension === "all" ? weightedAverage(group, (row) => rowAverage(row, "P")) : weightedAverage(group, (row) => row[`P_${state.dimension}`]),
      topGap: [...stats].sort((a, b) => b.gap - a.gap)[0]
    };
  });
}

function renderText() {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  $("#themeToggle span").textContent = state.theme === "dark" ? t("themeLight") : t("themeLabel");
}

function renderOptions() {
  const brands = [...new Set(rows.map((row) => row.brand))].sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));
  const series = [...new Set(rows.filter((row) => state.brand === "all" || row.brand === state.brand).map((row) => row.series))]
    .sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));

  $("#brandFilter").innerHTML = [`<option value="all">${t("allBrands")}</option>`, ...brands.map((brand) => `<option value="${brand}">${brand}</option>`)].join("");
  $("#brandFilter").value = state.brand;

  if (!series.includes(state.series)) state.series = "all";
  $("#seriesFilter").innerHTML = [`<option value="all">${t("allSeries")}</option>`, ...series.map((item) => `<option value="${item}">${item}</option>`)].join("");
  $("#seriesFilter").value = state.series;

  $("#dimensionFilter").innerHTML = [`<option value="all">${t("allDimensions")}</option>`, ...dimensions.map((dimension) => `<option value="${dimension}">${dimensionLabel(dimension)}</option>`)].join("");
  $("#dimensionFilter").value = state.dimension;
}

function renderMetrics(items) {
  const top = topGap(items);
  const totalSamples = items.reduce((sum, row) => sum + row.sample_count, 0);
  const brandCount = new Set(items.map((row) => row.brand)).size;
  const avgImportance = state.dimension === "all"
    ? weightedAverage(items, (row) => rowAverage(row, "I"))
    : weightedAverage(items, (row) => row[`I_${state.dimension}`]);
  const avgSatisfaction = state.dimension === "all"
    ? weightedAverage(items, (row) => rowAverage(row, "P"))
    : weightedAverage(items, (row) => row[`P_${state.dimension}`]);

  $("#metricCoverage").textContent = formatCount(totalSamples);
  $("#metricCoverageMeta").textContent = `${brandCount} ${t("brands")} · ${items.length} ${t("series")}`;
  $("#metricSatisfaction").textContent = score(avgImportance);
  $("#metricSatisfactionMeta").textContent = t("sourceImportance");
  $("#metricGap").textContent = score(avgSatisfaction);
  $("#metricGapMeta").textContent = t("sourcePerformance");
  $("#metricOpportunity").textContent = `${dimensionLabel(top.dimension)} ${score(top.gap)}`;
  $("#metricOpportunityMeta").textContent = t("largestDimensionGap");
  $("#signalHeadline").textContent = state.lang === "zh"
    ? `${dimensionLabel(top.dimension)}是当前最大差值：重要度 ${score(top.importance)}，满意度 ${score(top.satisfaction)}。`
    : `${dimensionLabel(top.dimension)} has the largest gap: importance ${score(top.importance)}, satisfaction ${score(top.satisfaction)}.`;
  $("#signalMeta").textContent = t("signalMeta");
}

function renderPortfolio(items) {
  const list = state.brand === "all" && state.series === "all"
    ? aggregateByBrand(items)
    : items.map((row) => {
        const stats = state.dimension === "all" ? dimensionStats([row]) : dimensionStats([row]).filter((item) => item.dimension === state.dimension);
        return {
          brand: `${row.brand} · ${row.series}`,
          series: 1,
          sample_count: row.sample_count,
          avgImportance: state.dimension === "all" ? rowAverage(row, "I") : row[`I_${state.dimension}`],
          avgSatisfaction: state.dimension === "all" ? rowAverage(row, "P") : row[`P_${state.dimension}`],
          topGap: [...stats].sort((a, b) => b.gap - a.gap)[0]
        };
      });

  const sorted = list.sort((a, b) => b.sample_count - a.sample_count);
  const maxSamples = Math.max(...sorted.map((item) => item.sample_count), 1);
  $("#portfolioStatus").textContent = `${sorted.length} ${t("filteredStatus")}`;
  $("#portfolioList").innerHTML = sorted.map((item) => `
    <div class="brand-row">
      <div class="brand-name">
        <strong>${item.brand}</strong>
        <span>${item.series} ${t("series")} · ${formatCount(item.sample_count)} ${t("samples")}</span>
      </div>
      <div>
        <div class="bar-track"><div class="bar-fill" style="width:${Math.max(3, item.sample_count / maxSamples * 100)}%"></div></div>
        <span class="bar-meta">${dimensionLabel(item.topGap.dimension)} ${t("gap")} ${score(item.topGap.gap)}</span>
      </div>
      <span class="score-badge">${t("avgImportance")} ${score(item.avgImportance)}</span>
      <span class="p-badge">${t("avgSatisfaction")} ${score(item.avgSatisfaction)}</span>
    </div>
  `).join("");
}

function renderRadar(items) {
  const stats = dimensionStats(items);
  const cx = 150;
  const cy = 150;
  const maxR = 104;
  const polygon = (field) => stats.map((item, index) => {
    const angle = (-90 + 360 / stats.length * index) * Math.PI / 180;
    return `${cx + Math.cos(angle) * maxR * item[field]},${cy + Math.sin(angle) * maxR * item[field]}`;
  }).join(" ");
  const grid = [0.25, 0.5, 0.75, 1].map((scale) => {
    const points = stats.map((_, index) => {
      const angle = (-90 + 360 / stats.length * index) * Math.PI / 180;
      return `${cx + Math.cos(angle) * maxR * scale},${cy + Math.sin(angle) * maxR * scale}`;
    }).join(" ");
    return `<polygon class="radar-grid" points="${points}"></polygon>`;
  }).join("");
  const labels = stats.map((item, index) => {
    const angle = (-90 + 360 / stats.length * index) * Math.PI / 180;
    return `<text class="radar-label" x="${cx + Math.cos(angle) * 130}" y="${cy + Math.sin(angle) * 130}" text-anchor="middle" dominant-baseline="middle">${dimensionLabel(item.dimension)}</text>`;
  }).join("");
  $("#radarChart").innerHTML = `${grid}<polygon class="radar-shape radar-importance" points="${polygon("importance")}"></polygon><polygon class="radar-shape radar-performance" points="${polygon("satisfaction")}"></polygon>${labels}`;
  $("#radarLegend").innerHTML = `
    <div class="legend-row"><span class="legend-swatch importance"></span><strong>${t("importanceLine")}</strong><span>${t("importanceMeaning")}</span></div>
    <div class="legend-row"><span class="legend-swatch satisfaction"></span><strong>${t("satisfactionLine")}</strong><span>${t("satisfactionMeaning")}</span></div>
  `;
}

function renderPriorities(items) {
  const stats = selectedStats(items).sort((a, b) => b.gap - a.gap).slice(0, 3);
  const samples = items.reduce((sum, row) => sum + row.sample_count, 0);
  $("#priorityBoard").innerHTML = stats.map((item, index) => {
    const label = index === 0 ? t("improve") : item.satisfaction >= 0.88 ? t("maintain") : t("monitor");
    return `
      <div class="priority-card">
        <span class="status-pill">${label}</span>
        <strong>${dimensionLabel(item.dimension)}</strong>
        <p>${t("avgImportance")} ${score(item.importance)} · ${t("avgSatisfaction")} ${score(item.satisfaction)}</p>
        <div class="priority-meta">
          <span>${t("gap")} ${score(item.gap)}</span>
          <span>${formatCount(samples)} ${t("samples")}</span>
        </div>
      </div>
    `;
  }).join("");
}

function renderMatrix(items) {
  const stats = dimensionStats(items);
  $("#ipaMatrix").innerHTML = `
    <span class="quadrant-label q1">${t("maintain")}</span>
    <span class="quadrant-label q2">${t("monitor")}</span>
    <span class="quadrant-label q3">${t("monitor")}</span>
    <span class="quadrant-label q4">${t("improve")}</span>
    ${stats.map((item) => {
      const x = Math.min(94, Math.max(6, (item.importance - 0.82) / 0.18 * 100));
      const y = 100 - Math.min(94, Math.max(6, (item.satisfaction - 0.62) / 0.36 * 100));
      return `<span class="matrix-point" style="left:${x}%; top:${y}%"></span><span class="matrix-label" style="left:${x}%; top:${y}%">${dimensionLabel(item.dimension)}</span>`;
    }).join("")}
  `;
}

function evidenceDimension(items) {
  return state.dimension === "all" ? topGap(items).dimension : state.dimension;
}

function renderEvidence(items) {
  const dimension = evidenceDimension(items);
  let candidates = evidenceRows.filter((row) => row.dimension === dimension);
  if (state.brand !== "all") candidates = candidates.filter((row) => row.brand === state.brand);
  if (state.series !== "all") candidates = candidates.filter((row) => row.series === state.series);
  if (candidates.length === 0 && state.brand !== "all") {
    candidates = evidenceRows.filter((row) => row.dimension === dimension);
  }
  const shown = candidates.slice(0, 4);
  $("#evidenceStatus").textContent = `${dimensionLabel(dimension)} · ${t("evidenceStatus")}`;
  $("#evidenceList").innerHTML = shown.length ? shown.map((row) => `
    <article class="evidence-card">
      <div>
        <strong>${row.brand} · ${row.series}</strong>
        <span>${row.review_date || "-"} · ${dimensionLabel(row.dimension)} ${row.score ? `${t("avgSatisfaction")} ${row.score}` : ""}</span>
      </div>
      <p>${row.text}</p>
    </article>
  `).join("") : `<p class="empty-state">${t("noEvidence")}</p>`;
}

function renderRecords(items) {
  const shown = [...items].sort((a, b) => b.sample_count - a.sample_count).slice(0, 12);
  $("#recordTable").innerHTML = shown.map((row) => {
    const stat = state.dimension === "all"
      ? [...dimensionStats([row])].sort((a, b) => b.gap - a.gap)[0]
      : dimensionStats([row]).find((item) => item.dimension === state.dimension);
    return `
      <div class="record-row">
        <strong>${row.brand} · ${row.series}</strong>
        <span>${row.sample_count} ${t("samples")}</span>
        <span>${dimensionLabel(stat.dimension)} ${t("avgImportance")} ${score(stat.importance)}</span>
        <span>${dimensionLabel(stat.dimension)} ${t("avgSatisfaction")} ${score(stat.satisfaction)}</span>
        <span>${t("gap")} ${score(stat.gap)}</span>
      </div>
    `;
  }).join("");
}

function renderTruth() {
  $("#truthBox").innerHTML = `
    <p>${t("truthBody")}</p>
    <ul>
      <li>${t("truthPoint1")}</li>
      <li>${t("truthPoint2")}</li>
      <li>${t("truthPoint3")}</li>
    </ul>
  `;
}

function renderBrief(items) {
  const top = topGap(items);
  $("#decisionBrief").innerHTML = `
    <div class="brief-callout">
      <strong>${t("briefTitle")}</strong>
      <p>${t("briefBody")}</p>
      <span class="status-pill">${dimensionLabel(top.dimension)} · ${t("gap")} ${score(top.gap)}</span>
    </div>
    <ul>
      <li>${t("action1")}</li>
      <li>${t("action2")}</li>
      <li>${t("action3")}</li>
    </ul>
  `;
}

function render() {
  renderText();
  renderOptions();
  const items = filteredRows();
  renderMetrics(items);
  renderPortfolio(items);
  renderRadar(items);
  renderPriorities(items);
  renderMatrix(items);
  renderEvidence(items);
  renderTruth();
  renderRecords(items);
  renderBrief(items);
}

function setupControls() {
  $("#brandFilter").addEventListener("change", (event) => {
    state.brand = event.target.value;
    state.series = "all";
    render();
  });
  $("#seriesFilter").addEventListener("change", (event) => {
    state.series = event.target.value;
    render();
  });
  $("#dimensionFilter").addEventListener("change", (event) => {
    state.dimension = event.target.value;
    render();
  });
  $("#themeToggle").addEventListener("click", () => {
    state.theme = state.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = state.theme;
    $("#themeToggle").setAttribute("aria-pressed", state.theme === "dark");
    renderText();
  });
  $("#langToggle").addEventListener("click", () => {
    state.lang = state.lang === "en" ? "zh" : "en";
    document.documentElement.lang = state.lang === "en" ? "en" : "zh-CN";
    $("#langToggle").setAttribute("aria-pressed", state.lang === "zh");
    render();
  });
}

function init() {
  setupControls();
  if (!Array.isArray(window.IPA_SOURCE_ROWS)) throw new Error("IPA data missing");
  rows = normalizeRows(window.IPA_SOURCE_ROWS);
  evidenceRows = Array.isArray(window.UGC_EVIDENCE_ROWS) ? window.UGC_EVIDENCE_ROWS : [];
  render();
}

init();
