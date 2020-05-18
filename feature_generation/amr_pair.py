def create_pair_labels(data):
    pairs = []
    for sentence_id, data in enumerate(data):
        tokens =  data.fields['tgt_tokens'].tokens[1:-1]
        head_indices = data.fields['head_indices'].labels
        labels = data.fields['head_tags'].labels
        
        for i, index in enumerate(head_indices):
            if (index != 0):
                parent = tokens[index-1]
                child = tokens[i]
                label = labels[i]
                pairs.append((sentence_id+1, str(parent), str(child),str(label)))
                
    return pairs

def find_label(data, pair_labels):
    for pair_label in pair_labels:
        sentence_id, label_parent, label_child, label = pair_label
        if (data['sentence_id'] == sentence_id and data['parent'] == label_parent and data['child']==label_child):
            return label
    return "unk"

def create_labels(pair_labels, sentence_dataset, with_flipped=False):
    labels = []
    unk_pairs = []
    pair_labels_dict = dict()
    not_found_count = 0
    found_count = 0
    
    for idx, data in sentence_dataset.iterrows():
        found = False
        flipped_found = False
        flipped_data = None
        
        if (data['sentence_id'] not in pair_labels_dict):
            pair_labels_dict[data['sentence_id']] = [pair_label for pair_label in pair_labels if pair_label[0] == data['sentence_id']]    
        cur_pair_labels = pair_labels_dict[data['sentence_id']]
            
        for pair_label in cur_pair_labels:
            _, label_parent, label_child, label = pair_label
            if (data['parent'].split('_')[0] == label_parent and data['child'].split('_')[0]==label_child):
                labels.append(label)
                found = True
                break

            elif with_flipped and (data['parent'].split('_')[0] == label_child and data['child'].split('_')[0]==label_parent):
                flipped_found = True
                flipped_data = (data['child'], data['parent'], label)
        
        if flipped_found and not found:
            sentence_dataset.loc[idx,'parent'] = flipped_data[0]
            sentence_dataset.loc[idx,'child'] = flipped_data[1]
            labels.append(flipped_data[2])
        
        if not flipped_found and not found:
            not_found_count += 1
            dependency_role = data['dependency_role'] 
            if (dependency_role in ['nsubj']):
                labels.append("ARG0")
            elif (dependency_role in ['obl', 'obj']):
                labels.append('ARG1')
            elif (dependency_role in ['case'] and data['child'] in ['di', 'ke', 'dari']):
                labels.append('location')
            else:
                labels.append("mod")

            unk_pairs.append((data['parent'], data['child'], dependency_role, data['sentence_id']))
        else:
            found_count += 1
    
    print("Found pairs: ", found_count)
    print("AMR Pair labels: ", len(pair_labels))
    print("Dependency Parser Pair labels: ", len(sentence_dataset))
    print("Not found: ", not_found_count)
    
    precision = found_count/len(sentence_dataset)
    recall = found_count/len(pair_labels)
    print("Pair Precision: ", precision)
    print("Pair Recall: ", recall)
    print("Pair F1: ", 2*((precision*recall)/(precision+recall)))
    
    return labels, unk_pairs