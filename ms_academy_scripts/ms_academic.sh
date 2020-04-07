#!/bin/bash
# @ECHO OFF

# DOC - attributes: https://docs.microsoft.com/en-gb/academic-services/project-academic-knowledge/reference-paper-entity-attributes#extended-metadata-attributes
# -----
# Id	Paper ID
# Ti	Normalized title
# AA.AuId:	Author ID
# AA.AuN:	Normalized author name
# CC:	Citation count
# CitCon:	Citation contexts
# D:	Date published in YYYY-MM-DD format
# DOI:	Digital Object Identifier
# S:	List of source URLs of the paper, sorted by relevance
# Y:	Year published
# E.CC:	Citation contexts
# IA: Inverted abstract:	List of abstract words and their corresponding position in the original abstract (e.g. [{"the":[0, 15, 30]}, {"brown":[1]}, {"fox":[2]}])
# Not supported - AW:	Unique, normalized words in abstract, excluding common/stopwords

attributes=
for attr in Id Ti AA.AuId AA.AuN CC CitCon D DOI S Y IA F.FId F.DFN
do
  if [[ ${attributes} == "" ]]; then
    attributes=${attr}
  else
    attributes=${attributes}%2C${attr}
  fi
done
mkdir -p top_authors
# List of top author IDs on CF by MS Academic
for author in 1986422195 2002483998 2781213378 2289542319 2435751034 2104401652 1988164005 2057138063 677921955 130248871 2148013773 219814910 2021640924 297969600 2086922657 2124832546 2031945151 2142756370 2167675492 329072426
do
  curl  -X GET "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=And(Composite(AA.AuId%3D${author})%2C%20Composite(F.FId%3D21569690))&model=latest&count=100&offset=0&attributes=${attributes}" -H "Ocp-Apim-Subscription-Key:${MS_ACADEMIC_API_KEY}" | python -m json.tool > top_authors/${author}.json
  sleep 1
done
