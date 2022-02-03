import sublime, sublime_plugin, string, random
from datetime import date
today = date.today()

# Define HTML code snippets
snippets = {
    "Accordion":
        {
        "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Accordion, ID = {r}, date = {t} --> <div class="accordion" id="accordion-{r}">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="card"> <div class="card-header" id="heading-{i}-{r}"> <h5 class="mb-0"> <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-{i}-{r}" aria-expanded="false" aria-controls="collapse-{i}-{r}"> {a} </button> </h5> </div> <div id="collapse-{i}-{r}" class="collapse" aria-labelledby="heading-{i}-{r}" data-parent="#accordion-{r}"> <div class="card-body">{b}</div> </div> </div> \n<!-- End of Item {i} --> ',
        "End": '</div> \n<!-- End of Accordion, ID = {r}, date = {t} --> \n\n'
        },
    "V-tabs":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Vertical tabs, ID = {r}, date = {t} --> <div class="row"> <div class="col-3 no-gutters">',
        "Nav-Start": '<div class="nav flex-column nav-pills" id="vtabs-{r}" role="tablist" aria-orientation="vertical">',
        "Nav-Repeat": '<a class="nav-link{c}" id="vtabs-{i}-{r}-tab" data-toggle="pill" href="#vtabs-{i}-{r}" role="tab" aria-controls="vtabs-{i}-{r}" aria-selected="{f}">{a}</a>',
        "Nav-End": '</div> </div> <div class="col-9 no-gutters"> <div class="tab-content" id="v-tabs-tabContent">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane card p-3 fade{c}" id="vtabs-{i}-{r}" role="tabpanel" aria-labelledby="vtabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
        "End": '</div> </div> </div> \n<!-- End of Vertical tabs, ID = {r}, date = {t} --> \n\n'
    },
    "H-tabs":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Horizontal tabs, ID = {r}, date = {t} -->',
        "Nav-Start": '<ul class="nav nav-pills mb-0" id="htabs-{r}" role="tablist">',
        "Nav-Repeat": '<li class="nav-item"><a class="nav-link{c}" id="htabs-{i}-{r}-tab" data-toggle="pill" href="#htabs-{i}-{r}" role="tab" aria-controls="htabs-{i}-{r}" aria-selected="{f}">{a}</a></li>',
        "Nav-End": '</ul><div class="tab-content card" id="pills-tabContent">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane p-3 fade{c}" id="htabs-{i}-{r}" role="tabpanel" aria-labelledby="htabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
        "End": '</div> \n<!-- End of Horizontal tabs, ID = {r}, date = {t} --> \n\n'
    },
    "Show":
    {
        "Start": '\n\n<!-- Start of Show/Hide interface, ID = {r}, date = {t} -->',
        "Repeat": '<p> <a class="btn btn-primary" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}">{a}</a> </p>\n<div class="collapse" id="show-{r}"> <div class="card card-body"><h5>{a}</h5>\n{b} <small><a class="btn-block btn btn-sm btn-light" class="text-center" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}">Hide</a></small> </div> </div>',
        "End": ' \n<!-- End of Show/Hide interface, ID = {r}, date = {t} -->\n\n'
    },
    "Card-Template":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of {n}, ID = {r}, date = {t} --> <div class="{cs}">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card{cr}{cc}">{ci}<div class="card-header{ch}"><h5 class="card-title{ct}">{ti}{tp}{a}{ts}</h5> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of {n}, ID = {r}, date = {t} -->\n\n'
    },
    "Box-Template":
    {
        "Start": '',
        "Repeat": '\n\n<!-- Start of {n}, date = {t} --> \n<div class="clearfix container-fluid"></div>\n<div class="card{cr}{cc}">{ci} <div class="card-body"><h4 class="card-title{ct}"><i aria-hidden="true" class="fa {ti}"></i> {tp}{a}{ts}</h4>{b}\n{bf}</div> </div> \n<!-- End of {n}, date = {t} -->\n\n',
        "End": ''
    },
    "Card-Group": {
        "Card-Start": 'card-group',
        "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
    },
    "Card-Deck": {
        "Card-Start": 'card-deck',
        "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
    },
    "Card-Images": {
        "Card-Start": 'card-deck',
        "Card-Img":'\n<!-- Start of Card Image --> \n<img class="img-fluid" src="https://via.placeholder.com/1024x768?text=Replace+Me" alt="">\n <!-- End of Card Image -->\n',
    },
    "Card-Rainbow": {
        "Card-Start": 'card-deck',
        "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
        "Card-Repeat": ' text-white',
        "Card-Title": ' text-white',
    },
    "Card-Columns": {
        "Card-Start": 'card-columns',
    },
    "Card-Primary": {
                "Card-Repeat": " mt-1 mb-1 border-primary",
                "Card-Header": " bg-primary",
                "Card-Title": " text-white",
            },
    "Card-Secondary": {
                "Card-Repeat": " mt-1 mb-1 border-secondary",
                "Card-Header": " bg-secondary",
                "Card-Title": " text-white",
            },
    "Card-Success": {
                "Card-Repeat": " mt-1 mb-1 border-success",
                "Card-Header": " bg-success",
                "Card-Title": " text-white",
            },
    "Card-Danger": {
                "Card-Repeat": " mt-1 mb-1 border-danger",
                "Card-Header": " bg-danger",
                "Card-Title": " text-white",
            },
    "Card-Warning": {
                "Card-Repeat": " mt-1 mb-1 border-warning",
                "Card-Header": " bg-warning",
                "Card-Title": " text-dark",
            },
    "Card-Info": {
                "Card-Repeat": " mt-1 mb-1 border-info",
                "Card-Header": " bg-info",
                "Card-Title": " text-white",
            },
    "Card-Light": {
                "Card-Repeat": " mt-1 mb-1 border-light",
                "Card-Header": " bg-light",
                "Card-Title": " text-dark",
            },
    "Card-Dark": {
                "Card-Repeat": " mt-1 mb-1 border-dark",
                "Card-Header": " bg-dark",
                "Card-Title": " text-white",
            },
    "Box-Think": {
                "Card-Repeat": " mt-1 mb-1",
                "Card-Title": " text-success",
                "Title-Icon": 'fa-lightbulb-o',
            },
    "Box-Read": {
                "Card-Repeat": " mt-1 mb-1",
                "Card-Title": " text-info",
                "Title-Icon": 'fa-book',
            },
    "Box-Important": {
                "Card-Repeat": " mt-1 mb-1",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-exclamation-triangle',
            },
    "Box-Reflect": {
                "Card-Repeat": " mt-1 mb-1",
                "Title-Prefix": "Reflection Activity - ",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-warning" role="alert"> Record your responses in your <em>Learner\'s Worksheet</em>. Bring this document with you to your next face-to-face class to discuss with your teacher and fellow students. </div>'
            },
    "Box-Discuss": {
                "Card-Repeat": " mt-1 mb-1",
                "Title-Prefix": "Discussion Activity - ",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-warning" role="alert"> Record your responses in the [exact name of discussion activity] forum that follows this content. </div>'
            }
}

colours = ('bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-info', 'bg-dark')

class BuildBootstrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, type):
        view = self.view
        for region in view.sel():
            if not region.empty():
                s = view.substr(region) # string of selected region
                t = bs_parser(s,type) # send string to parser
                view.replace(edit, region, t) # Update page content
                # self.view.run_command("select_all")
                # self.view.run_command("htmlprettify")
                # self.view.sel().clear()

def bs_parser(string, type):

    name = type
    print("name: ", name)
    items = string.split('<h5>')

    # Initiate Card properties.   Set as blank if undefined
    cardStart = snippets[type].get('Card-Start','')
    print("cardStart: ", cardStart)
    cardRepeat = snippets[type].get('Card-Repeat','')
    print("cardRepeat: ", cardRepeat)
    cardImg = snippets[type].get('Card-Img','')
    print("cardImg: ", cardImg)
    cardTitle = snippets[type].get('Card-Title','')
    print("cardTitle: ", cardTitle)
    cardColour = snippets[type].get('Card-Colour','')
    print("cardColour: ", cardColour)
    cardHeader = snippets[type].get('Card-Header','')
    print("cardHeader: ", cardHeader)
    titlePrefix = snippets[type].get('Title-Prefix','')
    print("titlePrefix: ", titlePrefix)
    titleSuffix = snippets[type].get('Title-Suffix','')
    print("titleSuffix: ", titleSuffix)
    titleIcon = snippets[type].get('Title-Icon','')
    print("titleIcon: ", titleIcon)
    boxFooter = snippets[type].get('Box-Footer','')
    print("boxFooter: ", boxFooter)

    #if properties are defined, use these


    #if I am a Card
    if (type.startswith('Box-')):
        type = 'Box-Template'

    # if I am a type of Card group
    if (type == "Card-Group" or type == "Card-Deck" or type == "Card-Images" or type == "Card-Rainbow"):
        if len(items) > 4:
            print("len(items): ", len(items))
            cardStart = snippets['Card-Columns']['Card-Start']
            print("cardStart: ", cardStart)

    #if I am a Card
    if (type.startswith('Card-')):
        type = 'Card-Template'

    new_str = items[0] # Content prior to first <h5>
    # Create random ID
    randomKey = random_key(6)
    # loop thorough items (as defind by <h5>)
    for idx, item in enumerate(items):
        i = str (idx)
        if idx == 0:
            # Built starting BS HTML
            new_str += snippets[type]['Start'].format(r=randomKey,t=today,n=name,cs=cardStart)
            # If I have top level nav (V-tabs or H-tabs)
            if "Nav-Start" in snippets[type].keys():
                new_str += snippets[type]['Nav-Start'].format(r=randomKey,n=name)
                for idx, item in enumerate(items):
                    i = str (idx)
                    tabState = ''
                    f = 'false'
                    sub_items = item.split('</h5>')
                    if idx == 1: # If I'm the first item
                        tabState = ' active show'
                        f = 'true'
                    if idx > 0:
                        new_str += snippets[type]['Nav-Repeat'].format(r=randomKey, i=i, a=sub_items[0], f=f,c=tabState,n=name)
                new_str += snippets[type]['Nav-End'].format(r=randomKey)
        else:
            # Build repeating items
            sub_items = item.split('</h5>')
            tabState = ''
            if idx == 1: # If I'm the first item
                tabState = ' active show'
            # rainbow items
            if name == 'Card-Rainbow':
                n = idx%len(colours) - 1
                cardColour = " " + colours[n]
                print("cardColour: ", cardColour)

            new_str += snippets[type]['Repeat'].format(r=randomKey, i=i, a=sub_items[0], b=sub_items[1],c=tabState,cr=cardRepeat,ch=cardHeader,ct=cardTitle,cc=cardColour,ci=cardImg,ti=titleIcon,tp=titlePrefix,ts=titleSuffix,n=name,t=today,bf=boxFooter)
    new_str += snippets[type]['End'].format(r=randomKey,t=today,n=name)

    # print("new_str: ", new_str)
    return new_str

def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key