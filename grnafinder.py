import re
import argparse

def regex_match_count(pattern, string):
    return len(re.findall(pattern, string))

def find_longest_common_substring(str1, str2):
    longest_match = ""
    len1, len2 = len(str1), len(str2)

    for i in range(len1):
        for j in range(len2):
            k = 0
            while i + k < len1 and j + k < len2 and str1[i + k] == str2[j + k]:
                k += 1
            if k > len(longest_match):
                longest_match = str1[i:i + k]

    return longest_match

def scripte(file_path1, file_path2, min_length):
    results = []

    with open(file_path1, 'r') as file1:
        yangban = ""
        str11 = ""
        mubiao = ""

        for line1 in file1:
            if line1.startswith(">"):
                yangban = line1.strip()
            else:
                str11 = line1.strip()

                with open(file_path2, 'r') as file2:
                    for line2 in file2:
                        if line2.startswith(">"):
                            mubiao = line2.strip()
                        else:
                            str12 = line2.strip()
                            str5 = str12.replace("T", "C")
                            str4 = str11.replace("T", "C")
                            str6 = str4.replace("G", "A")
                            str7 = str5.replace("G", "A")
                            str1 = str6
                            str2 = str7

                            if len(str1) >= min_length and len(str2) >= min_length:
                                longest_match = find_longest_common_substring(str1, str2)

                                if len(longest_match) >= min_length and len(longest_match) < 61:
                                    jiequ2_start = str2.find(longest_match)
                                    jiequ2_end = jiequ2_start + len(longest_match)
                                    jiequ1_start = str1.find(longest_match)
                                    jiequ1_end = jiequ1_start + len(longest_match)
                                    numc = regex_match_count(longest_match, str2)
                                    nummt = regex_match_count("T", longest_match)
                                    numyt = regex_match_count("T", str1[jiequ1_start:jiequ1_end])
                                    nummG = regex_match_count("G", longest_match)
                                    numyG = regex_match_count("G", str1[jiequ1_start:jiequ1_end])
                                    allt = 0
                                    allG = 0

                                    for k in range(nummt):
                                        firstT = longest_match.find("T", k)
                                        if str1[jiequ1_start + firstT] == "T":
                                            allt += 2

                                    for G in range(nummG):
                                        firstG = longest_match.find("G", G)
                                        if str1[jiequ1_start + firstG] == "G":
                                            allG += 2

                                    if allt == nummt and allG == nummG:
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
                                            str(numc)
                                        )
                                        results.append(result_entry)

    # Sort the results primarily by yangban and secondarily by str(jiequ1)
    sorted_results = sorted(results, key=lambda x: (x[0], int(x[1])))

    # Add headers
    header = "mRNA,start,end,sequences,minicircles,start,end,sequences,matched-length,matched-number"
    print(header)

    for result in sorted_results:
        ABC = ",".join(result)
        print(ABC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find common substrings in two files and sort primarily by yangban and secondarily by str(jiequ1).')
    parser.add_argument('mRNAs', help='Path to the first input file (mRNAs)')
    parser.add_argument('minicircles', help='Path to the second input file (minicircles)')
    parser.add_argument('-l', '--min_length', type=int, default=20,
                        help='Minimum length for matches (default: 20)')

    args = parser.parse_args()
    scripte(args.mRNAs, args.minicircles, args.min_length)
