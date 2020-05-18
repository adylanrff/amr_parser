def create_dependency_parser_feature(annotator, sentence, sentence_id=0):
    annotation = annotator.annotate(sentence)

    dependency_parser_feature = {
        'sentence_id': [],
        'parent': [], 
        'parent_position': [], 
        'child': [], 
        'child_position': [], 
        'is_root' : [],
        'sequence': [],
        'parent_ner': [],
        'child_ner': [],
        'parent_pos': [],
        'dependency_role': [],
        'child_pos': []
    }

    for idx, dependency in enumerate(annotation['dependency']):
        head = dependency['head']
        if (head != 0):
            head_idx = head-1
            dependency_parser_feature['sentence_id'].append(sentence_id)
            dependency_parser_feature['sequence'].append(idx+1)
            dependency_parser_feature['parent'].append(annotation['lemmas'][head_idx])
            dependency_parser_feature['parent_position'].append(head_idx)
            dependency_parser_feature['child'].append(annotation['lemmas'][idx])
            dependency_parser_feature['child_position'].append(annotation['lemmas'].index(annotation['lemmas'][idx]))
            dependency_parser_feature['is_root'].append(1 if annotation['dependency'][head_idx]['head'] == 0 else 0)
            dependency_parser_feature['parent_ner'].append(annotation['ner_tags'][head_idx])
            dependency_parser_feature['child_ner'].append(annotation['ner_tags'][idx])
            dependency_parser_feature['parent_pos'].append(annotation['pos_tags'][head_idx])
            dependency_parser_feature['child_pos'].append(annotation['pos_tags'][idx])
            dependency_parser_feature['dependency_role'].append(dependency['relation'])
            
    return dependency_parser_feature
