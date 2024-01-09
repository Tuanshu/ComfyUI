import json


def convert_to_api_format(internal_format):
    api_format = {}

    # 建立一個從link_id到(node_id, output_index)的映射
    link_map = {}
    for link in internal_format["links"]:
        link_id, from_node, from_slot, to_node, to_slot, _ = link
        link_map[link_id] = (str(from_node), from_slot)

    for node in internal_format["nodes"]:
        node_id = str(node["id"])
        api_node = {"class_type": node["type"], "inputs": {}, "_meta": {"title": node.get("properties", {}).get("Node name for S&R", "")}}

        # 處理inputs
        if "inputs" in node:
            for input in node["inputs"]:
                input_name = input["name"]
                link_id = input.get("link")
                if link_id is not None:
                    # 查找連接的節點和插槽
                    from_node, from_slot = link_map.get(link_id, (None, None))
                    if from_node is not None:
                        api_node["inputs"][input_name] = [from_node, from_slot]

        # 處理outputs (若需要)
        # ...

        api_format[node_id] = api_node

    return api_format


def convert_to_internal_format(api_format):
    # 實現將第二種格式轉換為第一種格式的邏輯
    # ...
    pass


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def main():
    # 讀取JSON檔案
    original_format = read_json('workflow_oriformat.json')
    api_format = read_json('workflow_api_api_format.json')

    # 轉換格式
    converted_to_api = convert_to_api_format(original_format)
    # converted_to_internal = convert_to_internal_format(api_format)
    json.dump(converted_to_api)
    # 比較結果
    is_consistent_api = converted_to_api == api_format
    # is_consistent_internal = converted_to_internal == original_format

    print(f"API format consistency: {is_consistent_api}")
    # print(f"Internal format consistency: {is_consistent_internal}")


if __name__ == "__main__":
    main()
