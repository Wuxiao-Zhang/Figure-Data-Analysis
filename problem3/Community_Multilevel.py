import json
import igraph as ig
import pandas as pd


# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# 构建图结构
def build_graph(data):
    # 创建图
    graph = ig.Graph()

    # 添加节点
    nodes = data["nodes"]
    node_names = [node["name"] for node in nodes]
    graph.add_vertices(node_names)

    # 添加边
    links = data["links"]
    edges = [(link["source"], link["target"]) for link in links]
    graph.add_edges(edges)

    return graph


# 社区检测
def detect_communities(graph):
    # 使用 multilevel 方法划分社区
    communities = graph.community_multilevel()
    return communities


# 保存结果到 CSV
def save_results_to_csv(graph, communities, output_file):
    # 获取节点和社区信息
    nodes = graph.vs["name"]
    community_ids = communities.membership

    # 获取边信息
    edges = graph.get_edgelist()
    edge_source = [graph.vs[edge[0]]["name"] for edge in edges]
    edge_target = [graph.vs[edge[1]]["name"] for edge in edges]

    # 创建 DataFrame
    node_df = pd.DataFrame({
        "node": nodes,
        "community": community_ids
    })

    edge_df = pd.DataFrame({
        "source": edge_source,
        "target": edge_target
    })

    # 合并节点和边信息
    result_df = pd.merge(edge_df, node_df, left_on="source", right_on="node", how="left")
    result_df = pd.merge(result_df, node_df, left_on="target", right_on="node", how="left", suffixes=("_source", "_target"))

    # 选择需要的列
    result_df = result_df[["source", "target", "community_source", "community_target"]]

    # 保存为 CSV
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 主函数
def main():
    # 输入文件路径
    input_file = "案例数据3.json"
    output_file = "partition_result.csv"

    # 加载数据
    data = load_json(input_file)

    # 构建图结构
    graph = build_graph(data)

    # 社区检测
    communities = detect_communities(graph)

    # 保存结果
    save_results_to_csv(graph, communities, output_file)
    print(f"社区划分结果已保存到 {output_file}")


# 运行主函数
if __name__ == "__main__":
    main()
