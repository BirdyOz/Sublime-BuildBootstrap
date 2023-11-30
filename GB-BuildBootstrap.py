import sublime, sublime_plugin, string, random, re
from datetime import date, time
today = date.today()

# Define HTML code snippets
snippets = {
    "Accordion":
        {
        "Start": '\n\n<!-- Start of Accordion, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n<div class="accordion clearfix w-100" id="accordion-{r}">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="card clearfix"> <div class="card-header" id="heading-{i}-{r}"> <h4 class="mb-0"> <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-{i}-{r}" aria-expanded="false" aria-controls="collapse-{i}-{r}"> {a} </button> </h4> </div> <div id="collapse-{i}-{r}" class="collapse" aria-labelledby="heading-{i}-{r}" data-parent="#accordion-{r}"> <div class="card-body">{b}</div> </div> </div> \n<!-- End of Item {i} --> ',
        "End": '</div> \n<!-- End of Accordion, ID = {r}, date = {t} --> \n\n'
        },
    "V-tabs":
    {
        "Start": '\n\n<!-- Start of Vertical tabs, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n<div class="row clearfix w-100"> <div class="col-3 no-gutters">',
        "Nav-Start": '<div class="nav flex-column nav-pills" id="vtabs-{r}" role="tablist" aria-orientation="vertical">',
        "Nav-Repeat": '<a class="nav-link{c}" id="vtabs-{i}-{r}-tab" data-toggle="pill" href="#vtabs-{i}-{r}" role="tab" aria-controls="vtabs-{i}-{r}" aria-selected="{f}">{a}</a>',
        "Nav-End": '</div> </div> <div class="col-9 no-gutters"> <div class="tab-content" id="v-tabs-tabContent">',
        "Repeat": '\n\n<!-- Start of Tab {i} --> <div class="tab-pane card clearfix p-3 fade{c}" id="vtabs-{i}-{r}" role="tabpanel" aria-labelledby="vtabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Tab {i} --> ',
        "End": '</div> </div> </div> \n<!-- End of Vertical tabs, ID = {r}, date = {t} --> \n\n'
    },
    "H-tabs":
    {
        "Start": '\n\n<!-- Start of Horizontal tabs, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n',
        "Nav-Start": '<ul class="nav nav-pills mb-0 clearfix w-100" id="htabs-{r}" role="tablist">',
        "Nav-Repeat": '<li class="nav-item"><a class="nav-link{c}" id="htabs-{i}-{r}-tab" data-toggle="pill" href="#htabs-{i}-{r}" role="tab" aria-controls="htabs-{i}-{r}" aria-selected="{f}">{a}</a></li>',
        "Nav-End": '</ul><div class="tab-content card" id="pills-tabContent">',
        "Repeat": '\n\n<!-- Start of Tab {i} --> <div class="tab-pane clearfix p-3 fade{c}" id="htabs-{i}-{r}" role="tabpanel" aria-labelledby="htabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Tab {i} --> ',
        "End": '</div> \n<!-- End of Horizontal tabs, ID = {r}, date = {t} --> \n\n'
    },
    "Show":
    {
        "Start": '\n\n<!-- Start of Show/Hide interface, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n',
        "Repeat": '<p> <a class="btn btn-primary" data-toggle="collapse" href="#show-{i}-{r}" role="button" aria-expanded="false" aria-controls="show-{i}-{r}">{a}</a> </p>\n<div class="collapse" id="show-{i}-{r}"> <div class="card clearfix card-body"><h4>{a}</h4>\n{b} <small><a class="btn-block btn btn-sm btn-light" class="text-center" data-toggle="collapse" href="#show-{i}-{r}" role="button" aria-expanded="false" aria-controls="show-{i}-{r}">Hide</a></small> </div> </div>',
        "End": ' \n<!-- End of Show/Hide interface, ID = {r}, date = {t} -->\n\n'
    },
    "Quote-Fancy-Card":
    {
        "Start": '\n\n<!-- Start of Fancy Quote, ID = {r}, date = {t} -->',
        "Repeat": '\n<blockquote class="blockquote clearfix card m-4 p-4 shadow rounded border-info col-10 mx-auto" style="margin-top: 2.5em !important">\n <div class="text-info" style="margin-top: -3.3em"> <span class="fa-stack fa-2x"> <i class="fa fa-circle fa-stack-2x"></i> <i class="fa fa-quote-left fa-stack-1x fa-inverse"></i> </span></div>\n <div class="lead">\n{a}\n <div class="blockquote-footer small text-muted text-right">{b}</div>\n</blockquote>',
        "End": ' \n<!-- End of Fancy Quote, ID = {r}, date = {t} -->\n\n'
    },
    "Quote-Fancy":
    {
        "Start": '\n\n<!-- Start of Fancy Quote Card, ID = {r}, date = {t} -->',
        "Repeat": '<blockquote class="blockquote m-4 border-light border-light"><i aria-hidden="true" class="fa fa-fw fa-quote-left fa-2x text fa-pull-left" style="color :lightgrey;"></i>\n <div class="lead">\n{a}\n </div> <i aria-hidden="true" class="fa fa-fw fa-quote-right fa-2x text fa-pull-right m-0" style="color:lightgrey;"></i>\n <div class="blockquote-footer small text-muted mt-4">{b}</div>\n</blockquote>',
        "End": ' \n<!-- End of Fancy Quote Card, ID = {r}, date = {t} -->\n\n'
    },
    "Card-Template":
    {
        "Start": '\n\n<!-- Start of {n}, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n <div class="clearfix w-100 {cs}">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card {cr} {cc} clearfix">{ci}<div class="card-header{ch}"><h4 class="card-title{ct}">{ti}{tp}{a}{ts}</h4> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of {n}, ID = {r}, date = {t} -->\n\n'
    },
    "Grid-Template":
    {
        "Start": '\n\n<!-- Start of {n}, ID = {r}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n<div class="clearfix w-100 row row-cols-1 {cs} m-1">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="col mb-4"> <div class="card h-100 {cr} {cc} clearfix"><div class="card-header{ch}"><h4 class="card-title{ct}">{ti}{tp}{a}{ts}</h4> </div> <div class="card-body">{b}</div> </div></div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of {n}, ID = {r}, date = {t} -->\n\n'
    },
    "Box-Template":
    {
        "Start": '',
        "Repeat": '\n\n<!-- Start of {n}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n<div class="card{cr}{cc} clearfix w-100">{ci} <div class="card-body"><h4 class="card-title{ct}"><i aria-hidden="true" class="fa {ti}"></i> {tp}{a}{ts}</h4>{b}\n{bf}</div> </div> \n<!-- End of {n}, date = {t} -->\n\n',
        "End": ''
    },
    "Alert-Template":
    {
        "Start": '',
        "Repeat": '\n\n<!-- Start of {n}, date = {t} -->\n<div class="clearfix container-fluid"></div>\n<div class="alert {cr} clearfix w-100" role="alert">\n{a}\n</div>\n<!-- End of {n}, date = {t} -->\n\n\n',
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
                "Title-Prefix": "Reflection Activity",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your <strong>Personal Reflective Journal </strong>. Your reflections will help you to understand the content and prepare for assessment</div>'
            },
    "Box-Discuss": {
                "Card-Repeat": " mt-1 mb-1",
                # "Title-Prefix": "Discussion Activity",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-success" role="alert"> Share your ideas with other learners, either in face-to-face discussion in the classroom, in the <strong>Topic [X] Discussion Forum</strong>, or as directed by your trainer.</div>'
            },
    "Box-Learning": {
                "Card-Repeat": " mt-1 mb-1",
                # "Title-Prefix": "Learning Activity",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your <strong>Learning Activity Worksheet </strong>. Your reflections will help you to understand the content and prepare for assessment. You might be asked to share your responses in class.</div>'
            },
    "Box-Law": {
                "Card-Repeat": " mt-1 mb-1",
                # "Title-Prefix": "Law/Standard",
                "Card-Title": " text-danger",
                "Title-Icon": 'fa-balance-scale'
                # "Box-Footer": '<div class="alert alert-success" role="alert"> Check with your workplace or library for a copy of this standard.</div>'
            },
    "Box-Portfolio": {
                "Card-Repeat": " mt-1 mb-1",
                "Title-Prefix": "Portfolio",
                "Card-Title": " text-success",
                "Title-Icon": 'fa-flag',
                "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your portfolio of evidence.</div>'
            },
    "Box-Info": {
                "Card-Repeat": " mt-1 mb-1",
                "Title-Prefix": "Further Information",
                "Card-Title": " text-success",
                "Title-Icon": 'fa-info-circle'
            },
    "Grid-2x": {
                "Card-Start": 'row-cols-md-2'
    },
    "Grid-3x": {
                "Card-Start": 'row-cols-xl-3 row-cols-lg-2'
    },
    "Grid-Rainbow-2x": {
                "Card-Start": 'row-cols-md-2',
                "Card-Repeat": ' text-white',
                "Card-Title": ' text-white',
    },
    "Grid-Rainbow-3x": {
                "Card-Start": 'row-cols-xl-3 row-cols-lg-2',
                "Card-Repeat": ' text-white',
                "Card-Title": ' text-white',
    }
}

colours = ('bg-primary', 'bg-info', 'bg-success', 'bg-danger',  'bg-dark', 'bg-secondary')

class BuildBootstrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, type):
        view = self.view
        for region in view.sel():
            if not region.empty():
                s = view.substr(region) # string of selected region
                scope = view.scope_name(view.sel()[0].begin())
                t = bs_parser(s,type) # send string to parser

                view.replace(edit, region, t) # Update page content
                self.view.run_command("htmlprettify")
                if 'text.html.markdown' in str(scope):
                    self.view.run_command("delete_empty_lines")
                self.view.sel().clear()

class QuickClickCommand(sublime_plugin.TextCommand):
    def run(self, edit, items):
        self.view.show_popup_menu(
            [item["caption"] for item in items],
            lambda idx: self.pick(idx, items))

    def pick(self, idx, items):
        if idx >= 0:
            command = items[idx].get("command")
            args = items[idx].get("args")
            self.view.window().run_command(command, args)


def bs_parser(string, type):

    name = type
    heading='h3'

    #if I am an Alert
    if (type.startswith('Alert-')):
        type = 'Alert-Template'
        heading='hx' # Prevent splitting

    #if I am a Fancy quote card
    if (type.startswith('Quote-')):
        heading='blockquote' # Prevent splitting

    # Initiate Card properties.   Set as blank if undefined
    cardStart = snippets[type].get('Card-Start','')
    cardRepeat = snippets[type].get('Card-Repeat','')
    cardImg = snippets[type].get('Card-Img','')
    cardTitle = snippets[type].get('Card-Title','')
    cardColour = snippets[type].get('Card-Colour','')
    cardHeader = snippets[type].get('Card-Header','')
    titlePrefix = tP = snippets[type].get('Title-Prefix','')
    titleSuffix = snippets[type].get('Title-Suffix','')
    titleIcon = snippets[type].get('Title-Icon','')
    boxFooter = snippets[type].get('Box-Footer','')




    # if I am a type of Card group
    if (type == "Card-Group" or type == "Card-Deck" or type == "Card-Images" or type == "Card-Rainbow"):
        if len(items) > 4:
            cardStart = snippets['Card-Columns']['Card-Start']

    #if I am a Card
    if (type.startswith('Card-')):
        type = 'Card-Template'

    #if I am a Grid
    if (type.startswith('Grid-')):
        type = 'Grid-Template'

    #if I am a Box
    if (type.startswith('Box-')):
        type = 'Box-Template'

    #if I am an Alert
    if (type.startswith('Alert-')):
        cardRepeat = name.lower()


    items = string.split('<{}>'.format(heading)) # Split on heading (if defined)

    new_str = items[0] # Content prior to first heading
    print("new_str: ", new_str)
    # Create random ID
    randomKey = random_key(6)
    # loop thorough items (as defind by heading)
    for idx, item in enumerate(items):
        i = str (idx)
        if idx == 0 and len(items)>1:
            print("idx: ", idx)
            # Built starting BS HTML
            new_str += snippets[type]['Start'].format(r=randomKey,t=today,n=name,cs=cardStart)
            # If I have top level nav (V-tabs or H-tabs)
            if "Nav-Start" in snippets[type].keys():
                new_str += snippets[type]['Nav-Start'].format(r=randomKey,n=name)
                for idx, item in enumerate(items):
                    i = str (idx)
                    tabState = ''
                    f = 'false'
                    sub_items = item.split('</{}>'.format(heading))
                    if idx == 1: # If I'm the first item
                        tabState = ' active show'
                        f = 'true'
                    if idx > 0:
                        new_str += snippets[type]['Nav-Repeat'].format(r=randomKey, i=i, a=sub_items[0], f=f,c=tabState,n=name)
                new_str += snippets[type]['Nav-End'].format(r=randomKey)
        else:
            # Build repeating items
            sub_items = item.split('</{}>'.format(heading))
            print("sub_items: ", sub_items)

            # If there was no </h3>
            if len(sub_items) == 1:
                sub_items.append('')
                new_str = ''


            tabState = ''
            if idx == 1: # If I'm the first item
                tabState = ' active show'
            # rainbow items
            if '-Rainbow' in name:
                n = idx%len(colours) - 1
                cardColour = " " + colours[n]
                print("cardColour: ", cardColour)

            # If heading text already starts with title prefix (for boxes etc)
            if (titlePrefix is not ''):
                print("sub_items[0]: ", sub_items[0])
                if(sub_items[0].startswith(titlePrefix)):
                    tP = ''
                else:
                    tP = titlePrefix + ' - '

            new_str += snippets[type]['Repeat'].format(r=randomKey, i=i, a=sub_items[0], b=sub_items[1],c=tabState,cr=cardRepeat,ch=cardHeader,ct=cardTitle,cc=cardColour,ci=cardImg,ti=titleIcon,tp=tP,ts=titleSuffix,n=name,t=today,bf=boxFooter)
    new_str += snippets[type]['End'].format(r=randomKey,t=today,n=name)
    new_str = re.sub('(?<!\.) {2,}',' ',new_str)


    return new_str

def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key