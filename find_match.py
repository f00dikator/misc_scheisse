import difflib

def main():
    # minimum_match_len = 5

    # open csv and identify which columns we have

    # for each searchable column within the csv (description, info, xrefs, etc.)

        # done = 0
        # search_text = None

        # if registry key check:
            # search_text = key
        # else if CMD_EXEC key check:
            # search_text = CMD
        # else if <whatever>
            # whatever
 
        # if search_text:
            # search existing audits for string
            # if we find a match:
                # print out the entire <custom_item> associated with check ID
                # done = 1

        # if done == 0:
            # best_match = None
            # best_match_count = 0
            # for each column that we are using as a comparison
                # for each similar_column in existing audits
                    #count = find_longest_match(csv_text, existing_audit_text)
                    #count_len = count[0]
                    #count_text = count[1]
                    #if count_len > minimum_match_len
                        # if count_len > best_match_count:
                            # best_match_count = count_len
                            # best_match = Unique ID for the existing check
                            # done = 1

           # if best_match not None
               # lookup the entire custom_item associated with check ID and print it
        # if done == 0:
            # put a placeholder in the audit file for this item 
                
    # close csv file



def find_longest_match(str1, str2):
    ret = [0, None]
    s = difflib.SequenceMatcher(None, str1, str2)
    s.get_matching_blocks()
    offset = s.find_longest_match(0, len(str1), 0, len(str2))[0]
    length = s.find_longest_match(0, len(str1), 0, len(str2))[2]
    if length > 0:
        ret = [ length, "Matched '{}' ({} chars)".format(str1[offset:(offset+length)],length)]
    
    return ret




if __name__ == "__main__":
    main()


