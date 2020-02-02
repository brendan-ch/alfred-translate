from workflow import Workflow3
import sys
import argparse
import json

# API_KEY = wf.get_password("alfred-translate")

with open("languages.json", "r") as languageFile:
  LANGUAGE_LIST = json.load(languageFile)

def getFullLanguage(code):
  languageFull = "automatic"

  for item in LANGUAGE_LIST:
    if (code == item["code"]): languageFull = item["name"]

  return languageFull

def setSource(source = None):
  # print(source)
  if (source != "detect" and source != None):
    for item in LANGUAGE_LIST:  # check if language code exists
      if (source.lower() == item["code"].lower()):
        wf.store_data("source-language", item["code"])  # saving from list ensures URL doesn't break
        break
  
  else:
    wf.store_data("source-language", None)  # set to automatic
  
  return 0

def setTarget(target):
  for item in LANGUAGE_LIST:  # check if language code exists
    if (target.lower() == item["code"].lower()):
      wf.store_data("target-language", item["code"])  # saving from list ensures URL doesn't break
      break

  return 0

def filterLanguages(query):
  def key_for_name(language):
    return '{}'.format(language['name'])

  items = wf.filter(query, LANGUAGE_LIST, key_for_name, min_score=64)
  first = False

  for item in items:
    if (not first):
      wf.add_item(title="%s (%s)" % (item['name'], item['code']), subtitle="Current source language: %s   Target language: %s" % (SOURCE_FULL, TARGET_FULL), valid=True, arg=item['code'])
    else:
      wf.add_item(title='%s (%s)' % (item['name'], item['code']), valid=True, arg=item['code'])
    
    first = True

  return 0


# def getTranslation(query, target, source = None):
#   if (source):
#     data = {"q": u"%s" % query, "source": "%s" % source, "target": "%s" % target, "format": "text"}

#   else:
#     data = {"q": u"%s" % query, "target": "%s" % target, "format": "text"}

#   result = requests.post("https://translation.googleapis.com/language/translate/v2?key=%s" % key, json=data)
#   converted_result = result.json()

#   translation = converted_result["data"]["translations"][0]["translatedText"]

def main(wf):
  import requests

  parser = argparse.ArgumentParser()
  parser.add_argument("--setkey", dest="setkey", nargs="?", const=None)  # set API key
  parser.add_argument("--setsource", dest="setsource", nargs="?", const="detect")  # set source language
  parser.add_argument("--settarget", dest="settarget", nargs="?", const="es")  # set target language
  parser.add_argument("--previewsource", dest="previewsource", nargs="?", const="detect")  # show preview of source & target languages
  parser.add_argument("--previewtarget", dest="previewtarget", nargs="?", const=None)
  parser.add_argument("--filterlanguages", dest="filterlanguages", nargs="?", const=None)  # not used
  parser.add_argument("--quickset", dest="quickset", nargs="+")  # quickly set source and target languages, 1 or 2 arguments
  parser.add_argument("query", nargs="?", default=None)
  args = parser.parse_args()

  if (args.setkey): wf.save_password("alfred-translate", str(args.setkey))  # save API key
  elif (args.setsource): setSource(args.setsource)  # set language source
  elif (args.settarget): setTarget(args.settarget)  # set language target

  elif (args.previewsource):

    if (args.previewsource == "detect"):
      wf.add_item(title='Automatic (detect source language)', subtitle="Current source language: %s   Target language: %s" % (SOURCE_FULL, TARGET_FULL), valid=True, arg=None)
    else: filterLanguages(args.previewsource)

  elif (args.previewtarget): filterLanguages(args.previewtarget)

  elif (args.quickset):

    if (len(args.quickset) == 2):
      setSource(args.quickset[0])
      setTarget(args.quickset[1])
    elif (len(args.quickset) == 1):
      setSource(None)
      setTarget(args.quickset[0])

  elif len(wf.args):  # "gt" command
    # with open("languages.json", "r") as languages:
    #   languageList = json.load(languages)

    try:
      key = wf.get_password("alfred-translate")
    except:
      wf.add_item(title="Unable to load API key.", subtitle='Please use keyword "gtkey" to set the API key.', valid=False, icon="1F433BB8-26C7-4F4D-97AD-2B6C0713A884.png")
      wf.add_item(title="Get API key from Google Cloud Platform", subtitle="You must create a project on GCP before getting a key.", valid=True, arg="https://console.cloud.google.com/apis/credentials", icon="link.png")
      wf.send_feedback()
      sys.exit(0)

    # source = wf.stored_data("source-language")
    # target = wf.stored_data("target-language")
    # sourceFull = getFullLanguage(source)
    # targetFull = getFullLanguage(target)
      
    # if (not target):
    #   target = wf.store_data("target-language", "es")
    #   target = "es"

    query = wf.args[0]

    if (query == ""):
      wf.add_item(title="Translate", subtitle="Current source language: %s   Target language: %s" % (SOURCE_FULL, TARGET_FULL), valid=False)
      wf.send_feedback()
      sys.exit(0)

    if (SOURCE):
      data = {"q": u"%s" % query, "source": "%s" % SOURCE, "target": "%s" % TARGET, "format": "text"}

    else:
      data = {"q": u"%s" % query, "target": "%s" % TARGET, "format": "text"}

    result = requests.post("https://translation.googleapis.com/language/translate/v2?key=%s" % key, json=data)
    converted_result = result.json()

    translation = converted_result["data"]["translations"][0]["translatedText"]

    if (SOURCE):
      wf.add_item(title=translation, subtitle="Current source language: %s   Target language: %s" % (SOURCE_FULL, TARGET_FULL), valid=True, arg="https://translate.google.com/#view=home&op=translate&sl=%s&tl=%s&text=%s" % (SOURCE, TARGET, query))
    else:
      wf.add_item(title=translation, subtitle="Current source language: %s   Target language: %s" % (getFullLanguage(converted_result["data"]["translations"][0]["detectedSourceLanguage"]), TARGET_FULL), valid=True, arg="https://translate.google.com/#view=home&op=translate&sl=auto&tl=%s&text=%s" % (TARGET, query))
  wf.send_feedback()
  return 0

if (__name__ == "__main__"):
  wf = Workflow3(libraries=['./lib'])

  SOURCE = wf.stored_data("source-language")
  TARGET = wf.stored_data("target-language")
  SOURCE_FULL = getFullLanguage(SOURCE)
  TARGET_FULL = getFullLanguage(TARGET)

  KEY = wf.get_password("alfred-translate")

  log = wf.logger
  sys.exit(wf.run(main))