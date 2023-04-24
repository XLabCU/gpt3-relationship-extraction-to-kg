# gpt3-relationship-extraction-to-kg

This repo hosts the code for Graham, Yates, and El-Roby 'Investigating Antiquities Trafficking with GPT-3 Enabled Knowledge Graphs: A Case Study'.

### OpenAI

Get a key for OpenAI, and save it to your machine's environment:

```
$ export OPENAI_API_KEY=[Your_GPT-3_API_KEY]
```

### Prepare your texts

Make sure that your input texts are small enough that they and the prompt can be passed to the OpenAI API; in practice we find around 6 kb is a good size.

Also make sure that each text file has the word `END` on its own line at the end of the file. You can do this at the command prompt with:

```
$ echo "END" >> *.txt
```

Then, run the bash script to resize the files:

```
$ sh split_resize.sh
```

### Extract Entities and Relationships

Run the extraction script from the command line:

```
 for file in test/*.txt; do python python_api.py training.txt $file >> output.txt; done
 ```
 
The code for `python_api.py` is via Sixing Huang, discussed at https://medium.com/geekculture/relationship-extraction-with-gpt-3-bb019dcf41e5 and  shared at https://github.com/dgg32/gpt-3-extract. MIT licensed. 

Because most of the results will be formatted like this:

```
 {"nodes": [
    {
      "Name": "Ducky",
      "type": "Object",
      "madeIn": "Ottawa",
      "date": "2023",
      "potter": "Mary Turlington",
      "painter": "Carol Holmes",
      "price": "$1 million"
    }

  ],
  "edges": [
    {
      "startNode": "Ducky",
      "endNode": "Ottawa-Civic Museum",
      "type": "bought by",
      "date": "2024"
     }
  ]
```

You should be able to find and fix any json errors quite quickly. [jsonlint.com](https://jsonlint.com/) is useful in this regard.

### Sample Output

Sample output for the article about [Aidonia](https://traffickingculture.org/encyclopedia/case-studies/aidonia-treasure/):

```
{
	"nodes": [{
			"Name": "Aidonia Treasure",
			"type": "Object",
			"returnedTo": "Greece",
			"date": "1996"
		},
		{
			"Name": "Mycenaean gold and jewelry",
			"type": "Object"
		},
		{
			"Name": "Aidonia",
			"type": "Place",
			"location": "Northeastern Peloponnesian district of Corinthia in Greece"
		},
		{
			"Name": "Mycenaean",
			"type": "Object",
			"date": "fifteenth-century BC"
		},
		{
			"Name": "archaiokapiloi",
			"type": "Organization",
			"role": "looters"
		},
		{
			"Name": "Greek Archaeological Service",
			"type": "Organization"
		},
		{
			"Name": "watermelons",
			"type": "Object"
		},
		{
			"Name": "Michael Ward Gallery",
			"type": "Organization"
		},
		{
			"Name": "John Betts",
			"type": "Individual",
			"role": "archaeologist"
		},
		{
			"Name": "Jack Ogden",
			"type": "Individual",
			"role": "Cambridge Centre for Precious Metal Research"
		},
		{
			"Name": "Greek Ministry of Culture",
			"type": "Organization"
		},
		{
			"Name": "Ricardo Elia",
			"type": "Individual",
			"role": "archaeologist"
		},
		{
			"Name": "James Wright",
			"type": "Individual",
			"role": "archaeologist"
		},
		{
			"Name": "New York Times",
			"type": "Organization"
		},
		{
			"Name": "Society for the Preservation of the Greek Heritage",
			"type": "Organization"
		},
		{
			"Name": "US District Court, Southern District of New York",
			"type": "Organization"
		},
		{
			"Name": "Athenian lawyer",
			"type": "Individual"
		},
		{
			"Name": "US$1. 5 million",
			"type": "Object"
		}
	],
	"edges": [{
			"startNode": "Aidonia Treasure",
			"endNode": "Greece",
			"type": "returned to",
			"date": "1996"
		},
		{
			"startNode": "Mycenaean gold and jewelry",
			"endNode": "Aidonia",
			"type": "robbed from",
			"date": "late 1970s"
		},
		{
			"startNode": "Mycenaean",
			"endNode": "Aidonia",
			"type": "discovered",
			"date": "November 1976"
		},
		{
			"startNode": "archaiokapiloi",
			"endNode": "Aidonia",
			"type": "looted",
			"date": "late 1970s"
		},
		{
			"startNode": "Greek Archaeological Service",
			"endNode": "Aidonia",
			"type": "assigned guard to",
			"date": "November 1977"
		},
		{
			"startNode": "watermelons",
			"endNode": "Greece",
			"type": "smuggled out of",
			"date": "late 1970s"
		},
		{
			"startNode": "Michael Ward Gallery",
			"endNode": "Mycenaean gold and jewelry",
			"type": "offered on display for sale",
			"date": "April 1993"
		},
		{
			"startNode": "John Betts",
			"endNode": "Mycenaean gold and jewelry",
			"type": "introduction and object descriptions",
			"date": "April 1993"
		},
		{
			"startNode": "Jack Ogden",
			"endNode": "Mycenaean gold and jewelry",
			"type": "gold analyses conducted",
			"date": "April 1993"
		},
		{
			"startNode": "Greek Ministry of Culture",
			"endNode": "Mycenaean gold and jewelry",
			"type": "confirmed not stolen",
			"date": "April 1993"
		},
		{
			"startNode": "Ricardo Elia",
			"endNode": "Mycenaean gold and jewelry",
			"type": "alerted the Consul General of Greece in New York",
			"date": "April 1993"
		},
		{
			"startNode": "James Wright",
			"endNode": "Mycenaean gold and jewelry",
			"type": "informed the Greek Archaeological Service of suspicion",
			"date": "April 1993"
		},
		{
			"startNode": "New York Times",
			"endNode": "Mycenaean gold and jewelry",
			"type": "described as 'rare gold baubles'",
			"date": "April 1993"
		},
		{
			"startNode": "Society for the Preservation of the Greek Heritage",
			"endNode": "Mycenaean gold and jewelry",
			"type": "returned to Greece",
			"date": "1996"
		},
		{
			"startNode": "US District Court, Southern District of New York",
			"endNode": "Mycenaean gold and jewelry",
			"type": "prevented sale or transport out of state",
			"date": "May 1993"
		}
	]
}
```

### Export to Cypher

Once you've tidied up any formatting errors, here is a Cypher query to load such json into Neo4j from a repo on github:

```
CALL apoc.periodic.iterate(" WITH 'https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/YOUR-REPO/main/YOUR-FILE.json' AS url CALL apoc.load.json(url) YIELD value UNWIND value.edges as r RETURN r", "WITH r.startNode AS startNode, r.endNode AS endNode, r.type AS type, r.properties AS properties MERGE (start:Node {name: startNode}) MERGE (end:Node {name: endNode}) MERGE (start)-[:`RELATION` {type: type}]->(end) FOREACH (prop IN properties | SET end += prop) RETURN start, end", {batchSize:1000, iterateList:true, parallel:true})
```

### To Ampligraph
[Ampligraph](https://docs.ampligraph.org/en/1.4.0/index.html) expects a csv file organized subject,predicate,object. Copy just the json output for the edges into a new document in your text editor. Use regular expressions to delete the extraneous keys etc so that you end up with three columns. Save the resulting CSV file with `UTF-8 with BOM` encoding. (This is because Excel will otherwise have trouble with various characters).

Make a copy of the file, and then open that copy in Excel. Rearrange the columns into subject, predicate, object order if you need to. Make a pivot table on the data, where the rows are the predicates and the value is the count of predicates. Sort that table from greatest to least. This will show you the frequency of various kinds of statements, which you can then use to rationalize the number of statements (replacing synonyms with just one consistent statement/phrase for instance). We open a new window with the pivot table displaying, and then use filters/sort on the data to guide the work of relabelling. We find that fewer than 100 different kinds of predicates gives best results.

Save the data sheet as utf-8 encoded csv. You can now import the data into Ampligraph. A fork of Ampligraph configured to work with Tensorflow 2 is at https://github.com/arylwen/AmpliGraph and can be imported into the Google Colab environment with:

```
!git clone https://github.com/arylwen/AmpliGraph.git
cd AmpliGraph
!pip install -e .
```


