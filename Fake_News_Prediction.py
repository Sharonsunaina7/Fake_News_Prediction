{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Logistic Regression is a fundamental and widely used statistical method for binary classification tasks. Despite its name, it's used for classification rather than regression."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "FaIBmnXCknPl"
   },
   "source": [
    "## Labels:\n",
    "           1: Fake News\n",
    "           0: Real News"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "k399dHafvL5N"
   },
   "source": [
    "## Importing the Dependencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "id": "-fetC5yqkPVe"
   },
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import re\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem.porter import PorterStemmer\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.metrics import accuracy_score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "1AC1YpmGwIDw",
    "outputId": "d726f6f2-2aae-4146-ae10-4776179d07d8"
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     C:\\Users\\LENOVO\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Unzipping corpora\\stopwords.zip.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import nltk\n",
    "nltk.download('stopwords')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "dxIOt3DowpUR",
    "outputId": "b3cf98ca-97a7-4635-aaa1-d6454a8759e0"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \"you're\", \"you've\", \"you'll\", \"you'd\", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', \"she's\", 'her', 'hers', 'herself', 'it', \"it's\", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', \"that'll\", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', \"don't\", 'should', \"should've\", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', \"aren't\", 'couldn', \"couldn't\", 'didn', \"didn't\", 'doesn', \"doesn't\", 'hadn', \"hadn't\", 'hasn', \"hasn't\", 'haven', \"haven't\", 'isn', \"isn't\", 'ma', 'mightn', \"mightn't\", 'mustn', \"mustn't\", 'needn', \"needn't\", 'shan', \"shan't\", 'shouldn', \"shouldn't\", 'wasn', \"wasn't\", 'weren', \"weren't\", 'won', \"won't\", 'wouldn', \"wouldn't\"]\n"
     ]
    }
   ],
   "source": [
    "# printing the stopwords in English\n",
    "print(stopwords.words('english'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "NjeGd1CLw_6R"
   },
   "source": [
    "## Data Pre-processing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "id": "nCGcpu_1wzLw"
   },
   "outputs": [],
   "source": [
    "# loading the dataset to a pandas DataFrame\n",
    "news_dataset = pd.read_csv(r\"C:\\Users\\LENOVO\\Desktop\\Skilligence AI-ML\\new task\\DataSets\\DataSets\\fake_news_train.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "aRgmbYSbxV4-",
    "outputId": "82bafe4f-211d-47b8-f4ed-a61b77370bc0"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(20800, 5)"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "news_dataset.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 198
    },
    "id": "jjJ1eB6RxZaS",
    "outputId": "9bb0c756-30e5-4919-a8e0-a688127261eb"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>title</th>\n",
       "      <th>author</th>\n",
       "      <th>text</th>\n",
       "      <th>label</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>House Dem Aide: We Didn’t Even See Comey’s Let...</td>\n",
       "      <td>Darrell Lucus</td>\n",
       "      <td>House Dem Aide: We Didn’t Even See Comey’s Let...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>FLYNN: Hillary Clinton, Big Woman on Campus - ...</td>\n",
       "      <td>Daniel J. Flynn</td>\n",
       "      <td>Ever get the feeling your life circles the rou...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>Why the Truth Might Get You Fired</td>\n",
       "      <td>Consortiumnews.com</td>\n",
       "      <td>Why the Truth Might Get You Fired October 29, ...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>15 Civilians Killed In Single US Airstrike Hav...</td>\n",
       "      <td>Jessica Purkiss</td>\n",
       "      <td>Videos 15 Civilians Killed In Single US Airstr...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>Iranian woman jailed for fictional unpublished...</td>\n",
       "      <td>Howard Portnoy</td>\n",
       "      <td>Print \\nAn Iranian woman has been sentenced to...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id                                              title              author  \\\n",
       "0   0  House Dem Aide: We Didn’t Even See Comey’s Let...       Darrell Lucus   \n",
       "1   1  FLYNN: Hillary Clinton, Big Woman on Campus - ...     Daniel J. Flynn   \n",
       "2   2                  Why the Truth Might Get You Fired  Consortiumnews.com   \n",
       "3   3  15 Civilians Killed In Single US Airstrike Hav...     Jessica Purkiss   \n",
       "4   4  Iranian woman jailed for fictional unpublished...      Howard Portnoy   \n",
       "\n",
       "                                                text  label  \n",
       "0  House Dem Aide: We Didn’t Even See Comey’s Let...      1  \n",
       "1  Ever get the feeling your life circles the rou...      0  \n",
       "2  Why the Truth Might Get You Fired October 29, ...      1  \n",
       "3  Videos 15 Civilians Killed In Single US Airstr...      1  \n",
       "4  Print \\nAn Iranian woman has been sentenced to...      1  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# print the first 5 rows of the dataframe\n",
    "news_dataset.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "QYkDi4SwxlKi",
    "outputId": "204c4b11-2d09-4c3e-ff1f-4ee9d3c5bc92"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "id           0\n",
       "title      558\n",
       "author    1957\n",
       "text        39\n",
       "label        0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# counting the number of missing values in the dataset\n",
    "news_dataset.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "id": "Mc04lQrhx57m"
   },
   "outputs": [],
   "source": [
    "# replacing the null values with empty string\n",
    "news_dataset = news_dataset.fillna('')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "id": "H7TZgHszygxj"
   },
   "outputs": [],
   "source": [
    "# merging the author name and news title\n",
    "news_dataset['content'] = news_dataset['author']+' '+news_dataset['title']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "cbF6GBBpzBey",
    "outputId": "f7776d4b-ab23-468c-8aa7-2ecbb67d7487"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0        Darrell Lucus House Dem Aide: We Didn’t Even S...\n",
      "1        Daniel J. Flynn FLYNN: Hillary Clinton, Big Wo...\n",
      "2        Consortiumnews.com Why the Truth Might Get You...\n",
      "3        Jessica Purkiss 15 Civilians Killed In Single ...\n",
      "4        Howard Portnoy Iranian woman jailed for fictio...\n",
      "                               ...                        \n",
      "20795    Jerome Hudson Rapper T.I.: Trump a ’Poster Chi...\n",
      "20796    Benjamin Hoffman N.F.L. Playoffs: Schedule, Ma...\n",
      "20797    Michael J. de la Merced and Rachel Abrams Macy...\n",
      "20798    Alex Ansary NATO, Russia To Hold Parallel Exer...\n",
      "20799              David Swanson What Keeps the F-35 Alive\n",
      "Name: content, Length: 20800, dtype: object\n"
     ]
    }
   ],
   "source": [
    "print(news_dataset['content'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "id": "LfBtAvLtzEo6"
   },
   "outputs": [],
   "source": [
    "# separating the data & label\n",
    "X = news_dataset.drop(columns='label', axis=1)\n",
    "Y = news_dataset['label']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "oHPBr540zl1h",
    "outputId": "45a8b684-6d35-43d4-f24f-8a8a091b69ad"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          id                                              title  \\\n",
      "0          0  House Dem Aide: We Didn’t Even See Comey’s Let...   \n",
      "1          1  FLYNN: Hillary Clinton, Big Woman on Campus - ...   \n",
      "2          2                  Why the Truth Might Get You Fired   \n",
      "3          3  15 Civilians Killed In Single US Airstrike Hav...   \n",
      "4          4  Iranian woman jailed for fictional unpublished...   \n",
      "...      ...                                                ...   \n",
      "20795  20795  Rapper T.I.: Trump a ’Poster Child For White S...   \n",
      "20796  20796  N.F.L. Playoffs: Schedule, Matchups and Odds -...   \n",
      "20797  20797  Macy’s Is Said to Receive Takeover Approach by...   \n",
      "20798  20798  NATO, Russia To Hold Parallel Exercises In Bal...   \n",
      "20799  20799                          What Keeps the F-35 Alive   \n",
      "\n",
      "                                          author  \\\n",
      "0                                  Darrell Lucus   \n",
      "1                                Daniel J. Flynn   \n",
      "2                             Consortiumnews.com   \n",
      "3                                Jessica Purkiss   \n",
      "4                                 Howard Portnoy   \n",
      "...                                          ...   \n",
      "20795                              Jerome Hudson   \n",
      "20796                           Benjamin Hoffman   \n",
      "20797  Michael J. de la Merced and Rachel Abrams   \n",
      "20798                                Alex Ansary   \n",
      "20799                              David Swanson   \n",
      "\n",
      "                                                    text  \\\n",
      "0      House Dem Aide: We Didn’t Even See Comey’s Let...   \n",
      "1      Ever get the feeling your life circles the rou...   \n",
      "2      Why the Truth Might Get You Fired October 29, ...   \n",
      "3      Videos 15 Civilians Killed In Single US Airstr...   \n",
      "4      Print \\nAn Iranian woman has been sentenced to...   \n",
      "...                                                  ...   \n",
      "20795  Rapper T. I. unloaded on black celebrities who...   \n",
      "20796  When the Green Bay Packers lost to the Washing...   \n",
      "20797  The Macy’s of today grew from the union of sev...   \n",
      "20798  NATO, Russia To Hold Parallel Exercises In Bal...   \n",
      "20799    David Swanson is an author, activist, journa...   \n",
      "\n",
      "                                                 content  \n",
      "0      Darrell Lucus House Dem Aide: We Didn’t Even S...  \n",
      "1      Daniel J. Flynn FLYNN: Hillary Clinton, Big Wo...  \n",
      "2      Consortiumnews.com Why the Truth Might Get You...  \n",
      "3      Jessica Purkiss 15 Civilians Killed In Single ...  \n",
      "4      Howard Portnoy Iranian woman jailed for fictio...  \n",
      "...                                                  ...  \n",
      "20795  Jerome Hudson Rapper T.I.: Trump a ’Poster Chi...  \n",
      "20796  Benjamin Hoffman N.F.L. Playoffs: Schedule, Ma...  \n",
      "20797  Michael J. de la Merced and Rachel Abrams Macy...  \n",
      "20798  Alex Ansary NATO, Russia To Hold Parallel Exer...  \n",
      "20799            David Swanson What Keeps the F-35 Alive  \n",
      "\n",
      "[20800 rows x 5 columns]\n",
      "0        1\n",
      "1        0\n",
      "2        1\n",
      "3        1\n",
      "4        1\n",
      "        ..\n",
      "20795    0\n",
      "20796    0\n",
      "20797    0\n",
      "20798    1\n",
      "20799    1\n",
      "Name: label, Length: 20800, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(X)\n",
    "print(Y)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "0NwFcpqcz37a"
   },
   "source": [
    "Stemming:\n",
    "\n",
    "Stemming is the process of reducing a word to its Root word\n",
    "\n",
    "example:\n",
    "actor, actress, acting --> act"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "id": "Ga_DaZxhzoWM"
   },
   "outputs": [],
   "source": [
    "port_stem = PorterStemmer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "id": "zY-n0dCh0e-y"
   },
   "outputs": [],
   "source": [
    "def stemming(content):\n",
    "    stemmed_content = re.sub('[^a-zA-Z]',' ',content) #Remove Non-Alphabetic Characters\n",
    "    stemmed_content = stemmed_content.lower() #Convert to Lowercase, for consistency\n",
    "    stemmed_content = stemmed_content.split() #Tokenization\n",
    "     #reducing words to their root\n",
    "    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]\n",
    "    stemmed_content = ' '.join(stemmed_content) #rejoins the stemmed tokens back into a single string\n",
    "    return stemmed_content"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "id": "MBUIk4c94yTL"
   },
   "outputs": [],
   "source": [
    "news_dataset['content'] = news_dataset['content'].apply(stemming)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "xmwK-zyO5Stg",
    "outputId": "61de12b9-b9fa-486f-8c91-a5aec48d7fe6"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0        darrel lucu hous dem aid even see comey letter...\n",
      "1        daniel j flynn flynn hillari clinton big woman...\n",
      "2                   consortiumnew com truth might get fire\n",
      "3        jessica purkiss civilian kill singl us airstri...\n",
      "4        howard portnoy iranian woman jail fiction unpu...\n",
      "                               ...                        \n",
      "20795    jerom hudson rapper trump poster child white s...\n",
      "20796    benjamin hoffman n f l playoff schedul matchup...\n",
      "20797    michael j de la merc rachel abram maci said re...\n",
      "20798    alex ansari nato russia hold parallel exercis ...\n",
      "20799                            david swanson keep f aliv\n",
      "Name: content, Length: 20800, dtype: object\n"
     ]
    }
   ],
   "source": [
    "print(news_dataset['content'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "id": "5ZIidnta5k5h"
   },
   "outputs": [],
   "source": [
    "#separating the data and label\n",
    "X = news_dataset['content'].values\n",
    "Y = news_dataset['label'].values"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "3nA_SBZX6BeH",
    "outputId": "3990e651-a18a-4191-c361-6854aa327caa"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['darrel lucu hous dem aid even see comey letter jason chaffetz tweet'\n",
      " 'daniel j flynn flynn hillari clinton big woman campu breitbart'\n",
      " 'consortiumnew com truth might get fire' ...\n",
      " 'michael j de la merc rachel abram maci said receiv takeov approach hudson bay new york time'\n",
      " 'alex ansari nato russia hold parallel exercis balkan'\n",
      " 'david swanson keep f aliv']\n"
     ]
    }
   ],
   "source": [
    "print(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "NgkFGXkg6HS4",
    "outputId": "c01c5aea-ece5-462b-f14f-a448409d0aa7"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1 0 1 ... 0 1 1]\n"
     ]
    }
   ],
   "source": [
    "print(Y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "Iu2ZEBkL6QTm",
    "outputId": "cbb35faa-bd75-4fee-a2ba-f85f874fe068"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(20800,)"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "id": "BMfepsQZ6TES"
   },
   "outputs": [],
   "source": [
    "# converting the textual data to numerical data\n",
    "vectorizer = TfidfVectorizer()\n",
    "vectorizer.fit(X)\n",
    "\n",
    "X = vectorizer.transform(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "MJj5esbs7Nzy",
    "outputId": "381f4859-7593-474e-a827-f1f4de5bd894"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<Compressed Sparse Row sparse matrix of dtype 'float64'\n",
      "\twith 210687 stored elements and shape (20800, 17128)>\n",
      "  Coords\tValues\n",
      "  (0, 267)\t0.2701012497770876\n",
      "  (0, 2483)\t0.36765196867972083\n",
      "  (0, 2959)\t0.24684501285337127\n",
      "  (0, 3600)\t0.3598939188262558\n",
      "  (0, 3792)\t0.27053324808454915\n",
      "  (0, 4973)\t0.23331696690935097\n",
      "  (0, 7005)\t0.2187416908935914\n",
      "  (0, 7692)\t0.24785219520671598\n",
      "  (0, 8630)\t0.2921251408704368\n",
      "  (0, 8909)\t0.36359638063260746\n",
      "  (0, 13473)\t0.2565896679337956\n",
      "  (0, 15686)\t0.2848506356272864\n",
      "  (1, 1497)\t0.2939891562094648\n",
      "  (1, 1894)\t0.15521974226349364\n",
      "  (1, 2223)\t0.3827320386859759\n",
      "  (1, 2813)\t0.19094574062359204\n",
      "  (1, 3568)\t0.26373768806048464\n",
      "  (1, 5503)\t0.7143299355715573\n",
      "  (1, 6816)\t0.1904660198296849\n",
      "  (1, 16799)\t0.30071745655510157\n",
      "  (2, 2943)\t0.3179886800654691\n",
      "  (2, 3103)\t0.46097489583229645\n",
      "  (2, 5389)\t0.3866530551182615\n",
      "  (2, 5968)\t0.3474613386728292\n",
      "  (2, 9620)\t0.49351492943649944\n",
      "  :\t:\n",
      "  (20797, 3643)\t0.2115550061362374\n",
      "  (20797, 7042)\t0.21799048897828685\n",
      "  (20797, 8364)\t0.22322585870464115\n",
      "  (20797, 8988)\t0.36160868928090795\n",
      "  (20797, 9518)\t0.29542040034203126\n",
      "  (20797, 9588)\t0.17455348025522197\n",
      "  (20797, 10306)\t0.08038079000566466\n",
      "  (20797, 12138)\t0.24778257724396505\n",
      "  (20797, 12344)\t0.27263457663336677\n",
      "  (20797, 13122)\t0.24825263521976057\n",
      "  (20797, 14967)\t0.3115945315488075\n",
      "  (20797, 15295)\t0.08159261204402356\n",
      "  (20797, 16996)\t0.08315655906109998\n",
      "  (20798, 350)\t0.2844693781907258\n",
      "  (20798, 588)\t0.3112141524638974\n",
      "  (20798, 1125)\t0.4460515589182237\n",
      "  (20798, 5032)\t0.40837014502395297\n",
      "  (20798, 6889)\t0.3249628569429943\n",
      "  (20798, 10177)\t0.31924963701870285\n",
      "  (20798, 11052)\t0.4460515589182237\n",
      "  (20798, 13046)\t0.2236326748827061\n",
      "  (20799, 377)\t0.5677577267055112\n",
      "  (20799, 3623)\t0.37927626273066584\n",
      "  (20799, 8036)\t0.45983893273780013\n",
      "  (20799, 14852)\t0.5677577267055112\n"
     ]
    }
   ],
   "source": [
    "print(X)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "mKBRGiSQ7YCZ"
   },
   "source": [
    "# Splitting the dataset to training & test data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "id": "VjMYwmBo7Pbx"
   },
   "outputs": [],
   "source": [
    "X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify=Y, random_state=2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "rxDsQvgO8Oln"
   },
   "source": [
    "## Training the Model: Logistic Regression"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "id": "HrSItcqc7qAy"
   },
   "outputs": [],
   "source": [
    "model = LogisticRegression()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "fdVJ839l8Vgx",
    "outputId": "129fab6a-f9d5-4ef8-eecf-93206f1e1e41"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {\n",
       "  /* Definition of color scheme common for light and dark mode */\n",
       "  --sklearn-color-text: black;\n",
       "  --sklearn-color-line: gray;\n",
       "  /* Definition of color scheme for unfitted estimators */\n",
       "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
       "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
       "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
       "  --sklearn-color-unfitted-level-3: chocolate;\n",
       "  /* Definition of color scheme for fitted estimators */\n",
       "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
       "  --sklearn-color-fitted-level-1: #d4ebff;\n",
       "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
       "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
       "\n",
       "  /* Specific color for light theme */\n",
       "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
       "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
       "  --sklearn-color-icon: #696969;\n",
       "\n",
       "  @media (prefers-color-scheme: dark) {\n",
       "    /* Redefinition of color scheme for dark theme */\n",
       "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
       "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
       "    --sklearn-color-icon: #878787;\n",
       "  }\n",
       "}\n",
       "\n",
       "#sk-container-id-1 {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 pre {\n",
       "  padding: 0;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-hidden--visually {\n",
       "  border: 0;\n",
       "  clip: rect(1px 1px 1px 1px);\n",
       "  clip: rect(1px, 1px, 1px, 1px);\n",
       "  height: 1px;\n",
       "  margin: -1px;\n",
       "  overflow: hidden;\n",
       "  padding: 0;\n",
       "  position: absolute;\n",
       "  width: 1px;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-dashed-wrapped {\n",
       "  border: 1px dashed var(--sklearn-color-line);\n",
       "  margin: 0 0.4em 0.5em 0.4em;\n",
       "  box-sizing: border-box;\n",
       "  padding-bottom: 0.4em;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-container {\n",
       "  /* jupyter's `normalize.less` sets `[hidden] { display: none; }`\n",
       "     but bootstrap.min.css set `[hidden] { display: none !important; }`\n",
       "     so we also need the `!important` here to be able to override the\n",
       "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
       "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
       "  display: inline-block !important;\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-text-repr-fallback {\n",
       "  display: none;\n",
       "}\n",
       "\n",
       "div.sk-parallel-item,\n",
       "div.sk-serial,\n",
       "div.sk-item {\n",
       "  /* draw centered vertical line to link estimators */\n",
       "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
       "  background-size: 2px 100%;\n",
       "  background-repeat: no-repeat;\n",
       "  background-position: center center;\n",
       "}\n",
       "\n",
       "/* Parallel-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item::after {\n",
       "  content: \"\";\n",
       "  width: 100%;\n",
       "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
       "  flex-grow: 1;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel {\n",
       "  display: flex;\n",
       "  align-items: stretch;\n",
       "  justify-content: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  position: relative;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:first-child::after {\n",
       "  align-self: flex-end;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:last-child::after {\n",
       "  align-self: flex-start;\n",
       "  width: 50%;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-parallel-item:only-child::after {\n",
       "  width: 0;\n",
       "}\n",
       "\n",
       "/* Serial-specific style estimator block */\n",
       "\n",
       "#sk-container-id-1 div.sk-serial {\n",
       "  display: flex;\n",
       "  flex-direction: column;\n",
       "  align-items: center;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  padding-right: 1em;\n",
       "  padding-left: 1em;\n",
       "}\n",
       "\n",
       "\n",
       "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
       "clickable and can be expanded/collapsed.\n",
       "- Pipeline and ColumnTransformer use this feature and define the default style\n",
       "- Estimators will overwrite some part of the style using the `sk-estimator` class\n",
       "*/\n",
       "\n",
       "/* Pipeline and ColumnTransformer style (default) */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable {\n",
       "  /* Default theme specific background. It is overwritten whether we have a\n",
       "  specific estimator or a Pipeline/ColumnTransformer */\n",
       "  background-color: var(--sklearn-color-background);\n",
       "}\n",
       "\n",
       "/* Toggleable label */\n",
       "#sk-container-id-1 label.sk-toggleable__label {\n",
       "  cursor: pointer;\n",
       "  display: block;\n",
       "  width: 100%;\n",
       "  margin-bottom: 0;\n",
       "  padding: 0.5em;\n",
       "  box-sizing: border-box;\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:before {\n",
       "  /* Arrow on the left of the label */\n",
       "  content: \"▸\";\n",
       "  float: left;\n",
       "  margin-right: 0.25em;\n",
       "  color: var(--sklearn-color-icon);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {\n",
       "  color: var(--sklearn-color-text);\n",
       "}\n",
       "\n",
       "/* Toggleable content - dropdown */\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content {\n",
       "  max-height: 0;\n",
       "  max-width: 0;\n",
       "  overflow: hidden;\n",
       "  text-align: left;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content pre {\n",
       "  margin: 0.2em;\n",
       "  border-radius: 0.25em;\n",
       "  color: var(--sklearn-color-text);\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-toggleable__content.fitted pre {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {\n",
       "  /* Expand drop-down */\n",
       "  max-height: 200px;\n",
       "  max-width: 100%;\n",
       "  overflow: auto;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {\n",
       "  content: \"▾\";\n",
       "}\n",
       "\n",
       "/* Pipeline/ColumnTransformer-specific style */\n",
       "\n",
       "#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator-specific style */\n",
       "\n",
       "/* Colorize estimator box */\n",
       "#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted input.sk-toggleable__control:checked~label.sk-toggleable__label {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label label.sk-toggleable__label,\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  /* The background is the default theme color */\n",
       "  color: var(--sklearn-color-text-on-default-background);\n",
       "}\n",
       "\n",
       "/* On hover, darken the color of the background */\n",
       "#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "/* Label box, darken color on hover, fitted */\n",
       "#sk-container-id-1 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
       "  color: var(--sklearn-color-text);\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Estimator label */\n",
       "\n",
       "#sk-container-id-1 div.sk-label label {\n",
       "  font-family: monospace;\n",
       "  font-weight: bold;\n",
       "  display: inline-block;\n",
       "  line-height: 1.2em;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-label-container {\n",
       "  text-align: center;\n",
       "}\n",
       "\n",
       "/* Estimator-specific */\n",
       "#sk-container-id-1 div.sk-estimator {\n",
       "  font-family: monospace;\n",
       "  border: 1px dotted var(--sklearn-color-border-box);\n",
       "  border-radius: 0.25em;\n",
       "  box-sizing: border-box;\n",
       "  margin-bottom: 0.5em;\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-0);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-0);\n",
       "}\n",
       "\n",
       "/* on hover */\n",
       "#sk-container-id-1 div.sk-estimator:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-2);\n",
       "}\n",
       "\n",
       "#sk-container-id-1 div.sk-estimator.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-2);\n",
       "}\n",
       "\n",
       "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
       "\n",
       "/* Common style for \"i\" and \"?\" */\n",
       "\n",
       ".sk-estimator-doc-link,\n",
       "a:link.sk-estimator-doc-link,\n",
       "a:visited.sk-estimator-doc-link {\n",
       "  float: right;\n",
       "  font-size: smaller;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1em;\n",
       "  height: 1em;\n",
       "  width: 1em;\n",
       "  text-decoration: none !important;\n",
       "  margin-left: 1ex;\n",
       "  /* unfitted */\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted,\n",
       "a:link.sk-estimator-doc-link.fitted,\n",
       "a:visited.sk-estimator-doc-link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
       ".sk-estimator-doc-link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover,\n",
       "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
       ".sk-estimator-doc-link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "/* Span, style for the box shown on hovering the info icon */\n",
       ".sk-estimator-doc-link span {\n",
       "  display: none;\n",
       "  z-index: 9999;\n",
       "  position: relative;\n",
       "  font-weight: normal;\n",
       "  right: .2ex;\n",
       "  padding: .5ex;\n",
       "  margin: .5ex;\n",
       "  width: min-content;\n",
       "  min-width: 20ex;\n",
       "  max-width: 50ex;\n",
       "  color: var(--sklearn-color-text);\n",
       "  box-shadow: 2pt 2pt 4pt #999;\n",
       "  /* unfitted */\n",
       "  background: var(--sklearn-color-unfitted-level-0);\n",
       "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link.fitted span {\n",
       "  /* fitted */\n",
       "  background: var(--sklearn-color-fitted-level-0);\n",
       "  border: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "\n",
       ".sk-estimator-doc-link:hover span {\n",
       "  display: block;\n",
       "}\n",
       "\n",
       "/* \"?\"-specific style due to the `<a>` HTML tag */\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link {\n",
       "  float: right;\n",
       "  font-size: 1rem;\n",
       "  line-height: 1em;\n",
       "  font-family: monospace;\n",
       "  background-color: var(--sklearn-color-background);\n",
       "  border-radius: 1rem;\n",
       "  height: 1rem;\n",
       "  width: 1rem;\n",
       "  text-decoration: none;\n",
       "  /* unfitted */\n",
       "  color: var(--sklearn-color-unfitted-level-1);\n",
       "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted {\n",
       "  /* fitted */\n",
       "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
       "  color: var(--sklearn-color-fitted-level-1);\n",
       "}\n",
       "\n",
       "/* On hover */\n",
       "#sk-container-id-1 a.estimator_doc_link:hover {\n",
       "  /* unfitted */\n",
       "  background-color: var(--sklearn-color-unfitted-level-3);\n",
       "  color: var(--sklearn-color-background);\n",
       "  text-decoration: none;\n",
       "}\n",
       "\n",
       "#sk-container-id-1 a.estimator_doc_link.fitted:hover {\n",
       "  /* fitted */\n",
       "  background-color: var(--sklearn-color-fitted-level-3);\n",
       "}\n",
       "</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>LogisticRegression()</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label fitted sk-toggleable__label-arrow fitted\">&nbsp;&nbsp;LogisticRegression<a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.5/modules/generated/sklearn.linear_model.LogisticRegression.html\">?<span>Documentation for LogisticRegression</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></label><div class=\"sk-toggleable__content fitted\"><pre>LogisticRegression()</pre></div> </div></div></div></div>"
      ],
      "text/plain": [
       "LogisticRegression()"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "sbPKIFT89W1C"
   },
   "source": [
    "# Evaluation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "YG6gqVty9ZDB"
   },
   "source": [
    "accuracy score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "id": "VgwtWZY59PBw"
   },
   "outputs": [],
   "source": [
    "# accuracy score on the training data\n",
    "X_train_prediction = model.predict(X_train)\n",
    "training_data_accuracy = accuracy_score(X_train_prediction, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "4L-r5mld-BFn",
    "outputId": "c662ccad-b5be-4f0c-e087-f8785e1a9141"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy score of the training data :  0.9863581730769231\n"
     ]
    }
   ],
   "source": [
    "print('Accuracy score of the training data : ', training_data_accuracy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {
    "id": "Kgcn13oO-H6e"
   },
   "outputs": [],
   "source": [
    "# accuracy score on the test data\n",
    "X_test_prediction = model.predict(X_test)\n",
    "test_data_accuracy = accuracy_score(X_test_prediction, Y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "9TG0Yof1-vg2",
    "outputId": "db5ab627-52bf-487c-df79-8d94647ffbe3"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy score of the test data :  0.9790865384615385\n"
     ]
    }
   ],
   "source": [
    "print('Accuracy score of the test data : ', test_data_accuracy)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "Yun4seaE-6tV"
   },
   "source": [
    "## Making a Predictive System"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "lPjssDL_-zo8",
    "outputId": "b8bcac5b-bab1-426c-ad89-d4791b411e31"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[0]\n",
      "The news is Real\n"
     ]
    }
   ],
   "source": [
    "X_new = X_test[3]\n",
    "\n",
    "prediction = model.predict(X_new)\n",
    "print(prediction)\n",
    "\n",
    "if (prediction[0]==0):\n",
    "  print('The news is Real')\n",
    "else:\n",
    "  print('The news is Fake')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "8KaWdvDI_eUk",
    "outputId": "49cf7c89-08b0-4ce3-8510-82efa7447d54"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0\n"
     ]
    }
   ],
   "source": [
    "print(Y_test[3])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {
    "id": "JBbWkLGr_lb_"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1]\n",
      "The news is Fake\n"
     ]
    }
   ],
   "source": [
    "X_new = X_test[77]\n",
    "\n",
    "prediction = model.predict(X_new)\n",
    "print(prediction)\n",
    "\n",
    "if (prediction[0]==0):\n",
    "  print('The news is Real')\n",
    "else:\n",
    "  print('The news is Fake')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1\n"
     ]
    }
   ],
   "source": [
    "print(Y_test[77])"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}