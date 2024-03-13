import re
import argparse

def regex_match_count(pattern, string):
    return len(re.findall(pattern, string))

def find_longest_common_substring(str1, str2, max_mismatches):
    longest_match = ""
    mismatches_count = 0
    match_start1 = match_start2 = 0
    len1, len2 = len(str1), len(str2)

    for i in range(len1):
        for j in range(len2):
            k, mismatches, last_mismatch = 0, 0, -2
            while i + k < len1 and j + k < len2:
                if str1[i + k] != str2[j + k]:
                    if mismatches >= max_mismatches or k == 0 or k == len1 - 1 or k - last_mismatch == 1:
                        break
                    mismatches += 1
                    last_mismatch = k
                k += 1
            if k > len(longest_match) and mismatches <= max_mismatches:
                longest_match = str1[i:i + k]
                mismatches_count = mismatches
                match_start1 = i
                match_start2 = j

    return longest_match, mismatches_count, match_start1, match_start2

def scripte(file_path1, file_path2, min_length, max_mismatches):
    results = []

    with open(file_path1, 'r') as file1:
        yangban = ""
        str11 = ""

        for line1 in file1:
            if line1.startswith(">"):
                yangban = line1.strip().lstrip('>')
            else:
                str11 = line1.strip()

                with open(file_path2, 'r') as file2:
                    for line2 in file2:
                        if line2.startswith(">"):
                            mubiao = line2.strip().lstrip('>')
                        else:
                            str12 = line2.strip()
                            str5 = str12.replace("T", "C")
                            str4 = str11.replace("T", "C")
                            str6 = str4.replace("G", "A")
                            str7 = str5.replace("G", "A")
                            str1 = str6
                            str2 = str7

                            if len(str1) >= min_length and len(str2) >= min_length:
                                longest_match, mismatches, match_start1, match_start2 = find_longest_common_substring(str1, str2, max_mismatches)

                                if len(longest_match) >= min_length and len(longest_match) < 61:
                                    jiequ1_start = match_start1
                                    jiequ1_end = jiequ1_start + len(longest_match)
                                    jiequ2_start = match_start2
                                    jiequ2_end = jiequ2_start + len(longest_match)

                                    result_entry = (
                                        yangban,
                                        str(jiequ1_start),
                                        str(jiequ1_end),
                                        str11[jiequ1_start:jiequ1_end],
                                        mubiao,
                                        str(jiequ2_start),
                                        str(jiequ2_end),
                                        str12[jiequ2_start:jiequ2_end],
                                        str(len(longest_match)),
                                        str(mismatches)
                                    )
                                    results.append(result_entry)

    # Sort the results primarily by yangban and secondarily by str(jiequ1_start)
    sorted_results = sorted(results, key=lambda x: (x[0], int(x[1])))

    # Add headers
    header = "mRNA,start,end,sequences,minicircles,start,end,sequences,matched-length,mismatches"
    print(header)

    for result in sorted_results:
        print(",".join(result))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find common substrings in two files with a specified number of mismatches.')
    parser.add_argument('mRNAs', help='Path to the first input file (mRNAs)')
    parser.add_argument('minicircles', help='Path to the second input file (minicircles)')
    parser.add_argument('-l', '--min_length', type=int, default=20, help='Minimum length for matches (default: 20)')
    parser.add_argument('-m', '--mismatches', type=int, default=1, choices=range(0, 6), help='Maximum number of mismatches allowed (0-5, default: 3)')

    args = parser.parse_args()
    scripte(args.mRNAs, args.minicircles, args.min_length, args.mismatches)
