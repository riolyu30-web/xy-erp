from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import json
import os
import sys
from fastapi import Depends
from fastapi.responses import StreamingResponse
from api.v1.dependencies import get_current_user
import pandas as pd
import io
from services.chroma_sercice import search_similar_fields_in_batch,get_model,search_similar_field
from services.neo4j_service import find_relation_path_logic,find_data_by_path
from services.tool import clear_data
from datawork.migrate_to_neo4j import clear_graph_database, rebuild_graph_database
from chroma_tool import build_chroma, clear_chroma
# 添加项目根目录到 sys.path，以便导入 codegen_tool
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

router = APIRouter()

@router.post("/clear-database")
async def clear_database():
    """
    清空并重新初始化 Neo4j 数据库。
    """
    try:
        clear_graph_database()
        return {"message": "Neo4j 数据库已成功清空。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空数据库时出错: {str(e)}")

@router.post("/rebuild-database")
async def rebuild_database():
    """
    完全重建 Neo4j 图数据库。
    """
    try:
        rebuild_graph_database()
        return {"message": "Neo4j 数据库已成功重建。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重建数据库时出错: {str(e)}")

@router.post("/build-vector/build-vector")
async def build_vector_collection():
    """
    构建向量数据库集合。
    """
    try:
        build_chroma()
        return {"message": "向量数据库集合已成功构建。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"构建向量数据库时出错: {str(e)}")

@router.post("/clear-vector")
async def clear_vector_collection():
    """
    清空向量数据库集合。
    """
    try:
        clear_chroma()
        return {"message": "向量数据库集合已成功清空。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空向量数据库时出错: {str(e)}")



model = get_model()

MCP_JSON_PATH = os.path.join(BASE_DIR, "mcp.json")
MCP_RELATION_PATH = os.path.join(BASE_DIR, "mcp_relation.json")
SCHEME_DIR_PATH = os.path.join(BASE_DIR, "scheme")

class HeaderInput(BaseModel):
    headers: list[str]

@router.post("/search")
async def upload_excel_header(item: HeaderInput):
    try:
        headers = item.headers
        similar_fields_map = search_similar_fields_in_batch(model, headers)

        if "message" not in similar_fields_map:
            raise HTTPException(status_code=400, detail=similar_fields_map)
       
        matched_fields = []
        for header in headers:
            field = similar_fields_map["message"].get(header)
            if field:
                matched_fields.append(field)

        relation_paths = find_relation_path_logic(matched_fields)
        if "message" not in relation_paths:
            raise HTTPException(status_code=400, detail=relation_paths)
        
        path_data_list = find_data_by_path(relation_paths["message"])
        
        if "message" not in path_data_list or not path_data_list["message"]:
            raise HTTPException(status_code=400, detail="未根据关系路径找到任何数据")
        reversed_fields = {v: k for k, v in similar_fields_map["message"].items() if v}
        path_clear_data_list = clear_data(path_data_list["message"], reversed_fields)
        return {"path_clear_data_list": path_clear_data_list,
            "path_data_list":path_data_list["message"],
            "reversed_fields":reversed_fields
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


class GuessInput(BaseModel):
    query: str

@router.post("/guess")
async def guess_field(item: GuessInput):
    try:
        similar_fields = search_similar_field(item.query)
        if similar_fields:
            return {"data": similar_fields}
        else:
            return {"message": "没有数据"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@router.get("/scheme/structure")
async def get_scheme_structure():

    structure = {}
    if not os.path.exists(SCHEME_DIR_PATH):
        return {}
    
    try:
        for root, dirs, files in os.walk(SCHEME_DIR_PATH):
            # 获取相对于 scheme 目录的路径作为 key
            relative_dir = os.path.relpath(root, SCHEME_DIR_PATH)
            # 在Windows上，路径分隔符是'\'，我们将其替换为'/'以保持一致性
            if os.sep != '/':
                relative_dir = relative_dir.replace(os.sep, '/')
            
            # 如果是根目录，使用'/'
            if relative_dir == '.':
                relative_dir = '/'

            json_files = [os.path.splitext(file)[0] for file in files if file.endswith('.json')]
            if json_files:
                structure[relative_dir] = json_files
        return structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scheme/content/{filename}")
async def get_scheme_content_by_filename(filename: str):
    SCHEME_DIR_PATH = os.path.join(BASE_DIR, "scheme")
    
    if not filename.endswith(".json"):
        filename += ".json"

    if ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid path components.")

    found_path = None
    if os.path.exists(SCHEME_DIR_PATH):
        for root, dirs, files in os.walk(SCHEME_DIR_PATH):
            if filename in files:
                found_path = os.path.join(root, filename)
                break
    
    if not found_path:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found in scheme directory.")

    try:
        with open(found_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/relation")
async def get_mcp_relation():
    try:
        if os.path.exists(MCP_RELATION_PATH):
            with open(MCP_RELATION_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

