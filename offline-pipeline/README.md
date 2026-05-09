# offline-pipeline

`offline-pipeline` 是仓库中的离线研究流水线模块，负责把新能源乘用车市场的公开参数、用户口碑与分析结果整理成可复用的数据资产。

## 系统演示

### 用户画像聚类结果

<p align="center">
  <img src="../docs/images/persona-clusters.png" alt="用户画像可视化" width="75%">
</p>

### IPA 战略分析矩阵

<p align="center">
  <img src="../docs/images/ipa-matrix.png" alt="IPA 分析图" width="75%">
</p>

### RAG 问答系统界面

<p align="center">
  <img src="../docs/images/rag-interface.png" alt="RAG 界面截图" width="75%">
</p>

---

## 模块组成

- `crawler/`
  采集车型参数、UGC 口碑和图片原始素材。
- `process/`
  清洗与标准化采集结果，输出统一结构的 `ugc.csv`、`vehicles_config.json`、`image_map.json`。
- `analysis/`
  进行用户画像聚类与 IPA（Importance-Performance Analysis）诊断。
- `graph/`
  把规格、画像、评论关系构造成 Neo4j 知识图谱。
- `vector/`
  把评论、规格与画像嵌入 ChromaDB，供检索与 RAG 使用。
- `rag/`
  基于 Chainlit 的交互式研究问答界面。
- `data/`
  存放原始数据、处理结果、分析产物和向量库。

## 推荐执行顺序

```bash
# 1. 重新构建向量库
python offline-pipeline/vector/build_vector_db.py

# 2. 构建知识图谱
python offline-pipeline/graph/build_graph.py

# 3. 如需重新采集
python offline-pipeline/crawler/Parameter_crawler.py
python offline-pipeline/crawler/UGC_crawler.py
python offline-pipeline/crawler/Picture_crawler.py

# 4. 如需重新清洗
python offline-pipeline/process/Para_process.py
python offline-pipeline/process/UGC_process.py
python offline-pipeline/process/Pic_process.py

# 5. 画像分析
python offline-pipeline/analysis/Persona/step1_extract_attention.py
python offline-pipeline/analysis/Persona/step3_final_clustering.py
python offline-pipeline/analysis/Persona/step4_merge_external_attributes.py

# 6. IPA 诊断
python offline-pipeline/analysis/IPA/step1_compute_scores.py
python offline-pipeline/analysis/IPA/step2_generate_ipa_reports.py

# 7. 启动研究问答
cd offline-pipeline/rag
chainlit run app.py
```

## 数据目录

```text
offline-pipeline/
├── crawler/
├── process/
├── analysis/
├── graph/
├── vector/
├── rag/
└── data/
    ├── Raw/
    ├── Processed/
    ├── Analyzed/
    ├── Vector/
    └── UGC_Vector_chroma/
```

## 说明

- `dashboard/` 中数据来源于本流程产出；
- `nev-product-research/` 参考本流程方法，但不直接复用脚本和数据。
