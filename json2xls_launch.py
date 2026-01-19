import os
import json
import pandas as pd
from typing import List, Dict, Any

### 这里定义列表头信息
Listup = ['App-ID','App-Name','App-Slug','Launch-ID','Launch-CreatedTime','Launch-Slug','Launch-Name','Launch-Tagline','Launch-FeaturedTime','Launch-LastDayScore']
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
        # A: data->product->id
        A = data.get('data', {}).get('product', {}).get('id', '')
        
        # B: data->product->name
        B = data.get('data', {}).get('product', {}).get('name', '')
        C = data.get('data', {}).get('product', {}).get('slug', '')
    except Exception as e:
        print(f"从文件 {json_path} 提取A/B属性时出错: {e}")
        return []
    
    # 遍历posts->edges下的每个元素
    try:
        edges = data.get('data', {}).get('product', {}).get('posts', {}).get('edges', [])
        
        for edge in edges:
            node = edge.get('node', {})
            
            # C: node->name
            D = node.get('id', '')
            E = node.get('createdAt', '')
            F = node.get('slug', '')
            G = node.get('name', '')
            H = node.get('tagline', '')
            I = node.get('featuredAt', '')
            if I == None:
                I = "null"
            J = node.get('launchDayScore','')
            
            # 添加到结果列表
            extracted_data.append({
                Listup[0]: A,
                Listup[1]: B,
                Listup[2]: C,
                Listup[3]: D,
                Listup[4]: E,
                Listup[5]: F,
                Listup[6]: G,
                Listup[7]: H,
                Listup[8]: I,
                Listup[9]: J,
            })
            
    except Exception as e:
        print(f"从文件 {json_path} 提取产品数据时出错: {e}")
    
    return extracted_data

def main():
    # 设置工作目录
    work_dir = "./launches/"
    
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
    df = pd.DataFrame(all_data, columns=Listup)
    
    # 写入Excel文件
    output_file = "Launches页（三层）.xls"
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