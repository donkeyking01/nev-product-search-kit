"""
Graph Retriever Tool - 图谱检索工具修复版本
执行 Cypher 查询获取结构化数据

Author: EV PM DSS Team
Date: 2026-02-16 - FIXED: Persona query schema
"""

from typing import List, Dict, Optional
from rag.config import get_graph_client


class GraphRetriever:
    """图谱检索工具"""
    
    def __init__(self):
        self.client = get_graph_client()
    
    def get_all_personas(self) -> List[Dict]:
        """
        获取所有用户画像（修复版）
        
        Returns:
            List of all persona insights with top dimensions
        """
        cypher = """
        MATCH (p:Persona)
        OPTIONAL MATCH (p)-[r:PRIORITIZES]->(d:Dimension)
        WITH p, r, d
        ORDER BY r.weight DESC
        WITH p, collect({dimension: d.name_cn, weight: r.weight})[..3] AS top_dimensions
        RETURN p.name AS persona_name,
               p.user_count AS review_count,
               top_dimensions
        """
        
        try:
            print(f"🔍 正在查询所有用户画像")
            results = self.client.query(cypher)
            print(f"   ✅ 查询到 {len(results)} 个画像")
            
            # 为每个结果添加描述
            for result in results:
                result['description'] = f"用户画像: {result.get('persona_name', 'Unknown')}"
                
            return results
        except Exception as e:
            print(f"❌ Error querying personas: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    # ... rest of the file remains the same ...
