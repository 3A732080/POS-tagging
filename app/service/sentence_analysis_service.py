import spacy
from helper.base_define import dump
from helper.base_define import data_get
from vector_db.query_data import is_empty_result, semantic_search
from graph.base_define import Shape


class SentenceAnalysis:
    # def __init__(self):

    def single_word(self, text):
        # 使用 spaCy 分詞、匹配
        nlp = spacy.load("en_core_web_md")
        doc = nlp(text)

        table_list = {
            'diamond': {},
            'entity': {}
        }

        value_list = []

        for token in doc: # 輸出每個詞彙的文本、通用詞性和詳細詞性
            dump("文字: " + token.text)

            # 用 Table 尋找
            temp = semantic_search(
                "Table",
                ["name", "ref { tag, shape, search_default_column }"],
                token.text
            )

            # 匹配到 Table
            if is_empty_result(temp, 'Table') == False:
                ref_temp = temp['data']['Get']['Table'][0]['ref']
                shape_temp = ref_temp['shape']
                name_temp = temp['data']['Get']['Table'][0]['name']
                idTemp = temp['data']['Get']['Table'][0]['_additional']['id']

                table_list[shape_temp][name_temp] = {
                    'id' : idTemp,
                    'ref': ref_temp
                }

                continue

            # 用 Value 尋找
            temp = semantic_search(
                "Value",
                ["name", "ref { tag, table, table_shape, column }"],
                token.text
            )

            # 匹配到 Value
            if is_empty_result(temp, 'Value') == False:
                value_list.append(
                    {
                        'name': temp['data']['Get']['Value'][0]['name'],
                        'id' : temp['data']['Get']['Value'][0]['_additional']['id'],
                        'ref': temp['data']['Get']['Value'][0]['ref']
                    }
                )
                continue

            # 用 Column 尋找
            temp = semantic_search(
                "Column",
                ["name", "ref { tag, table }"],
                token.text
            )

            # 匹配到 Column
            if is_empty_result(temp, 'Column') == False:
                name_temp = temp['data']['Get']['Column'][0]['name']
                table_list[Shape.predicate.value][name_temp] = {
                    'id' : temp['data']['Get']['Column'][0]['_additional']['id'],
                    'ref': temp['data']['Get']['Column'][0]['ref']
                }
                continue

            # 三種情況皆無
            dump("空空賞")

            # 待修正：考量四種匹配情境（3 種情境同時匹配、2 種情境匹配、只有1種、都沒有的時候）
            # 待修正：辨識是否存在
                # 1. 「否定」的情境（如：are not located in Paris、do not supply red parts）--> fEre: A(affirm)/ N(no)
                # 2. 「所有」的情境（如：supply all red parts）--> fNe: ∀(all)/ ∃(exist)

        return {
            "table_list": table_list,
            "value_list": value_list
        }

    def clause(self, text):
        return self.__process_and_annotate_sentence(text)

    def __process_and_annotate_sentence(self, text):
        # 使用 spaCy 分詞、匹配
        nlp = spacy.load("en_core_web_md")
        doc = nlp(text)

        # Flags for main clause
        main_clause_negation = False
        main_clause_all = False
        conditions = []
        has_subclause = False

        # Detect 'all' in the main clause by checking tokens outside any subclause
        main_clause_tokens = [token.text.lower() for token in doc if not list(token.ancestors) or all(ancestor.dep_ != 'relcl' for ancestor in token.ancestors)]
        if "all" in main_clause_tokens:
            main_clause_all = True

        # Process each token in the document
        for token in doc:
            # Check for negation in the main clause
            if token.dep_ == "neg" and not any(ancestor.dep_ == "relcl" for ancestor in token.ancestors):
                main_clause_negation = True

            # Process relative clauses ('relcl' dependency)
            if token.dep_ == "relcl":
                has_subclause = True
                clause = " ".join([tok.text for tok in token.subtree])
                modified_noun = token.head.text

                # Directly determine negation and "all" within the subclause
                conditions.append((clause, modified_noun))

        split_conditions = self.__split_and_annotate_conditions(conditions)

        # Print annotations
        self.__print_annotations(main_clause_negation, main_clause_all, split_conditions, has_subclause)

        return split_conditions


    def __split_and_annotate_conditions(self, conditions):
        split_conditions = []
        for condition, modified_noun in conditions:
            if ' or ' in condition:
                parts = condition.split(' or ')
                split_conditions.extend([(part.strip(), modified_noun) for part in parts])
            elif ' and ' in condition:
                parts = condition.split(' and ')
                split_conditions.extend([(part.strip(), modified_noun) for part in parts])
            else:
                split_conditions.append((condition, modified_noun))

        return self.__identify_negation_and_all(split_conditions)

    def __identify_negation_and_all(self, split_conditions):
        annotated_conditions = []

        for condition, modified_noun in split_conditions:
            negation = "not" in condition.lower()
            all_quantifier = "all" in condition.lower()
            annotation = {
                "condition": condition,
                "modified_noun": modified_noun,
                "negation": negation,
                "all": all_quantifier
            }
            annotated_conditions.append(annotation)

        return annotated_conditions

    def __print_annotations(self, main_clause_negation, main_clause_all, annotated_conditions, has_subclause):
        dump(f"句子主體註記：\n否定：{main_clause_negation}，包含 'all'：{main_clause_all}")

        if has_subclause:
            dump("\n子句的條件、修飾詞彙及註記：")

            for annotation in annotated_conditions:
                dump(f"條件：'{annotation['condition']}'，修飾的詞彙：{annotation['modified_noun']}，否定：{annotation['negation']}，包含 'all'：{annotation['all']}")
        else:
            dump("\n子句是否存在：False")


