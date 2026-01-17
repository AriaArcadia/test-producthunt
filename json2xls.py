import os
import json
import pandas as pd
from typing import List, Dict, Any

def extract_data_from_json(json_path: str) -> List[Dict[str, Any]]:
    """
    从单个JSON文件中提取所需数据
    
    Args:
        json_path: JSON文件路径
        
    Returns:
        包含提取数据的字典列表
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件 {json_path} 时出错: {e}")
        return []
    
    extracted_data = []
    
    # 获取A和B属性
    try:
        # A: data->productCategory->slug
        A = data.get('data', {}).get('productCategory', {}).get('slug', '')
        
        # B: data->productCategory->path
        # 注意：您的要求中写的是"productCategory-path"，但根据JSON结构可能是"path"
        B = data.get('data', {}).get('productCategory', {}).get('path', '')
    except Exception as e:
        print(f"从文件 {json_path} 提取A/B属性时出错: {e}")
        return []
    
    # 遍历products->edges下的每个元素
    try:
        edges = data.get('data', {}).get('productCategory', {}).get('products', {}).get('edges', [])
        
        for edge in edges:
            node = edge.get('node', {})
            
            # C: node->name
            C = node.get('name', '')
            
            # D: node->postsCount
            D = node.get('postsCount', '')
            
            # E: node->slug
            E = node.get('slug', '')
            
            # 添加到结果列表
            extracted_data.append({
                'Item': A,
                'Item-Path': B,
                'App-Name': C,
                'Launches-Counts': D,
                'App-Path': E
            })
            
    except Exception as e:
        print(f"从文件 {json_path} 提取产品数据时出错: {e}")
    
    return extracted_data

def main():
    # 设置工作目录
    work_dir = "./apps/"
    
    # 检查目录是否存在
    if not os.path.exists(work_dir):
        print(f"目录 {work_dir} 不存在！")
        return
    
    # 存储所有提取的数据
    all_data = []
    
    # 遍历工作目录下的所有JSON文件
    json_count = 0
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                print(f"处理文件: {json_path}")
                
                # 提取数据
                extracted_data = extract_data_from_json(json_path)
                all_data.extend(extracted_data)
                
                json_count += 1
    
    print(f"\n共处理 {json_count} 个JSON文件")
    print(f"提取到 {len(all_data)} 行数据")
    
    if not all_data:
        print("未提取到任何数据，请检查JSON文件格式！")
        return
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(all_data, columns=['Item', 'Item-Path', 'App-Name', 'Launches-Counts', 'App-Path'])
    
    # 写入Excel文件
    output_file = "APP页（二层）.xls"
    try:
        # 使用xlsxwriter引擎，确保写入.xls文件
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
            
            # 调整列宽（可选）
            worksheet = writer.sheets['Data']
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, min(column_width, 50))
        
        print(f"数据已成功写入 {output_file}")
        
    except Exception as e:
        print(f"写入Excel文件时出错: {e}")
        
        # 如果xlsxwriter不可用，尝试openpyxl
        try:
            df.to_excel("output.xlsx", index=False)
            print("数据已成功写入 output.xlsx (使用openpyxl引擎)")
        except Exception as e2:
            print(f"使用openpyxl引擎也失败: {e2}")
            
            # 作为最后手段，尝试写入CSV
            df.to_csv("output.csv", index=False, encoding='utf-8-sig')
            print("数据已成功写入 output.csv (CSV格式)")

if __name__ == "__main__":
    main()