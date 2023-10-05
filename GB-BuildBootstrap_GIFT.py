import sublime, sublime_plugin, string, random
from datetime import date, time
today = date.today()

# Define HTML code snippets
::Q01:: snippets = {
    ~ "Accordion":
    ~ ::Q02::         {
    ~ ::Q03::         "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Accordion, ID = {r}, date = {t} --> <div class="accordion" id="accordion-{r}">',
    ~ ::Q04::         "Repeat": '\n\n<!-- Start of Item {i} --> <div class="card clearfix"> <div class="card-header" id="heading-{i}-{r}"> <h4 class="mb-0"> <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-{i}-{r}" aria-expanded="false" aria-controls="collapse-{i}-{r}"> {a} </button> </h4> </div> <div id="collapse-{i}-{r}" class="collapse" aria-labelledby="heading-{i}-{r}" data-parent="#accordion-{r}"> <div class="card-body">{b}</div> </div> </div> \n<!-- End of Item {i} --> ',
    ~ ::Q05::         "End": '</div> \n<!-- End of Accordion, ID = {r}, date = {t} --> \n\n'
    ~ },
    ~ "V-tabs":
    ~ ::Q06::     {
    ~ ::Q07::         "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Vertical tabs, ID = {r}, date = {t} --> <div class="row"> <div class="col-3 no-gutters">',
    ~ ::Q08::         "Nav-Start": '<div class="nav flex-column nav-pills" id="vtabs-{r}" role="tablist" aria-orientation="vertical">',
    ~ ::Q09::         "Nav-Repeat": '<a class="nav-link{c}" id="vtabs-{i}-{r}-tab" data-toggle="pill" href="#vtabs-{i}-{r}" role="tab" aria-controls="vtabs-{i}-{r}" aria-selected="{f}">{a}</a>',
    ~ "Nav-End": '</div> </div> <div class="col-9 no-gutters"> <div class="tab-content" id="v-tabs-tabContent">',
    ~ ::Q10::         "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane card clearfix p-3 fade{c}" id="vtabs-{i}-{r}" role="tabpanel" aria-labelledby="vtabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
    ~ ::Q11::         "End": '</div> </div> </div> \n<!-- End of Vertical tabs, ID = {r}, date = {t} --> \n\n'
    ~ },
    ~ "H-tabs":
    ~ ::Q12::     {
    ~ ::Q13::         "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of Horizontal tabs, ID = {r}, date = {t} -->',
    ~ ::Q14::         "Nav-Start": '<ul class="nav nav-pills mb-0" id="htabs-{r}" role="tablist">',
    ~ ::Q15::         "Nav-Repeat": '<li class="nav-item"><a class="nav-link{c}" id="htabs-{i}-{r}-tab" data-toggle="pill" href="#htabs-{i}-{r}" role="tab" aria-controls="htabs-{i}-{r}" aria-selected="{f}">{a}</a></li>',
    ~ "Nav-End": '</ul><div class="tab-content card" id="pills-tabContent">',
    ~ ::Q16::         "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane clearfix p-3 fade{c}" id="htabs-{i}-{r}" role="tabpanel" aria-labelledby="htabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
    ~ ::Q17::         "End": '</div> \n<!-- End of Horizontal tabs, ID = {r}, date = {t} --> \n\n'
    ~ },
    ~ "Show":
    ~ ::Q18::     {
    ~ ::Q19::         "Start": '\n\n<!-- Start of Show/Hide interface, ID = {r}, date = {t} -->',
    ~ ::Q20::         "Repeat": '<p> <a class="btn btn-primary" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}">{a}</a> </p>\n<div class="collapse" id="show-{r}"> <div class="card clearfix card-body"><h4>{a}</h4>\n{b} <small><a class="btn-block btn btn-sm btn-light" class="text-center" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}">Hide</a></small> </div> </div>',
    ~ ::Q21::         "End": ' \n<!-- End of Show/Hide interface, ID = {r}, date = {t} -->\n\n'
    ~ },
    ~ "Card-Template":
    ~ ::Q22::     {
    ~ ::Q23::         "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of {n}, ID = {r}, date = {t} --> <div class="{cs}">',
    ~ ::Q24::         "Repeat": '\n\n<!-- Start of card {i} --> <div class="card {cr} {cc} clearfix">{ci}<div class="card-header{ch}"><h4 class="card-title{ct}">{ti}{tp}{a}{ts}</h4> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
    ~ ::Q25::         "End": '</div> \n<!-- End of {n}, ID = {r}, date = {t} -->\n\n'
    ~ },
    ~ "Grid-Template":
    ~ ::Q26::     {
    ~ ::Q27::         "Start": '\n<div class="clearfix container-fluid"></div>\n\n<!-- Start of {n}, ID = {r}, date = {t} --> <div class="row row-cols-1 row-cols-md-3 m-1">',
    ~ ::Q28::         "Repeat": '\n\n<!-- Start of card {i} --> <div class="col mb-4"> <div class="card h-100 {cr} {cc} clearfix"><div class="card-header{ch}"><h4 class="card-title{ct}">{ti}{tp}{a}{ts}</h4> </div> <div class="card-body">{b}</div> </div></div> \n<!-- End of card {i} --> ',
    ~ ::Q29::         "End": '</div> \n<!-- End of {n}, ID = {r}, date = {t} -->\n\n'
    ~ },
    ~ "Box-Template":
    ~ ::Q30::     {
    ~ "Start": '',
    ~ ::Q31::         "Repeat": '\n\n<!-- Start of {n}, date = {t} --> \n<div class="clearfix container-fluid"></div>\n<div class="card{cr}{cc} clearfix">{ci} <div class="card-body"><h4 class="card-title{ct}"><i aria-hidden="true" class="fa {ti}"></i> {tp}{a}{ts}</h4>{b}\n{bf}</div> </div> \n<!-- End of {n}, date = {t} -->\n\n',
    ~ "End": ''
    ~ },
    ~ "Alert-Template":
    ~ ::Q32::     {
    ~ "Start": '',
    ~ ::Q33::         "Repeat": '\n\n<!-- Start of {n}, date = {t} --> \n<div class="clearfix container-fluid"></div>\n<div class="alert {cr}" role="alert">\n{a}\n</div>\n<!-- End of {n}, date = {t} -->\n\n',
    ~ "End": ''
    ~ },
    ~ ::Q34::     "Card-Group": {
    ~ "Card-Start": 'card-group',
    ~ "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
    ~ },
    ~ ::Q35::     "Card-Deck": {
    ~ "Card-Start": 'card-deck',
    ~ "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
    ~ },
    ~ ::Q36::     "Card-Images": {
    ~ "Card-Start": 'card-deck',
    ~ "Card-Img":'\n<!-- Start of Card Image --> \n<img class="img-fluid" src="https://via.placeholder.com/1024x768?text=Replace+Me" alt="">\n <!-- End of Card Image -->\n',
    ~ },
    ~ ::Q37::     "Card-Rainbow": {
    ~ "Card-Start": 'card-deck',
    ~ "Card-Img":'\n<!-- OPTIONAL - Insert Card image here if needed -->\n',
    ~ "Card-Repeat": ' text-white',
    ~ "Card-Title": ' text-white',
    ~ },
    ~ ::Q38::     "Card-Columns": {
    ~ "Card-Start": 'card-columns',
    ~ },
    ~ ::Q39::     "Card-Primary": {
    ~ "Card-Repeat": " mt-1 mb-1 border-primary",
    ~ "Card-Header": " bg-primary",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q40::     "Card-Secondary": {
    ~ "Card-Repeat": " mt-1 mb-1 border-secondary",
    ~ "Card-Header": " bg-secondary",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q41::     "Card-Success": {
    ~ "Card-Repeat": " mt-1 mb-1 border-success",
    ~ "Card-Header": " bg-success",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q42::     "Card-Danger": {
    ~ "Card-Repeat": " mt-1 mb-1 border-danger",
    ~ "Card-Header": " bg-danger",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q43::     "Card-Warning": {
    ~ "Card-Repeat": " mt-1 mb-1 border-warning",
    ~ "Card-Header": " bg-warning",
    ~ "Card-Title": " text-dark",
    ~ },
    ~ ::Q44::     "Card-Info": {
    ~ "Card-Repeat": " mt-1 mb-1 border-info",
    ~ "Card-Header": " bg-info",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q45::     "Card-Light": {
    ~ "Card-Repeat": " mt-1 mb-1 border-light",
    ~ "Card-Header": " bg-light",
    ~ "Card-Title": " text-dark",
    ~ },
    ~ ::Q46::     "Card-Dark": {
    ~ "Card-Repeat": " mt-1 mb-1 border-dark",
    ~ "Card-Header": " bg-dark",
    ~ "Card-Title": " text-white",
    ~ },
    ~ ::Q47::     "Box-Think": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Card-Title": " text-success",
    ~ "Title-Icon": 'fa-lightbulb-o',
    ~ },
    ~ ::Q48::     "Box-Read": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Card-Title": " text-info",
    ~ "Title-Icon": 'fa-book',
    ~ },
    ~ ::Q49::     "Box-Important": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Card-Title": " text-danger",
    ~ "Title-Icon": 'fa-exclamation-triangle',
    ~ },
    ~ ::Q50::     "Box-Reflect": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Title-Prefix": "Reflection Activity",
    ~ "Card-Title": " text-danger",
    ~ "Title-Icon": 'fa-tasks',
    ~ "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your <strong>Personal Reflective Journal </strong>. Your reflections will help you to understand the content and prepare for assessment</div>'
    ~ },
    ~ ::Q51::     "Box-Discuss": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Title-Prefix": "Discussion Activity",
    ~ "Card-Title": " text-danger",
    ~ "Title-Icon": 'fa-tasks',
    ~ "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in the [exact name of discussion activity] forum that follows this content. </div>'
    ~ },
    ~ ::Q52::     "Box-Learning": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Title-Prefix": "Learning Activity",
    ~ "Card-Title": " text-danger",
    ~ "Title-Icon": 'fa-tasks',
    ~ "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your <strong>Learning Activity Worksheet </strong>. Your reflections will help you to understand the content and prepare for assessment. You might be asked to share your responses in class.</div>'
    ~ },
    ~ ::Q53::     "Box-Law": {
    ~ "Card-Repeat": " mt-1 mb-1",
    # "Title-Prefix": "Law/Standard",
    ~ "Card-Title": " text-danger",
    ~ "Title-Icon": 'fa-balance-scale'
    # "Box-Footer": '<div class="alert alert-success" role="alert"> Check with your workplace or library for a copy of this standard.</div>'
    ~ },
    ~ ::Q54::     "Box-Portfolio": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Title-Prefix": "Portfolio",
    ~ "Card-Title": " text-success",
    ~ "Title-Icon": 'fa-flag',
    ~ "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in your portfolio of evidence.</div>'
    ~ },
    ~ ::Q55::     "Box-Info": {
    ~ "Card-Repeat": " mt-1 mb-1",
    ~ "Title-Prefix": "Further Information",
    ~ "Card-Title": " text-success",
    ~ "Title-Icon": 'fa-info-circle'
    ~ }
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
    print("name: ", name)
    items = string.split('<h3>')
    print("items: ", items)

    #if I am an Alert
    if (type.startswith('Alert-')):
        type = 'Alert-Template'

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

    new_str = items[0] # Content prior to first <h3>
    print("new_str: ", new_str)
    # Create random ID
    randomKey = random_key(6)
    # loop thorough items (as defind by <h3>)
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
                    sub_items = item.split('</h3>')
                    if idx == 1: # If I'm the first item
                        tabState = ' active show'
                        f = 'true'
                    if idx > 0:
                        new_str += snippets[type]['Nav-Repeat'].format(r=randomKey, i=i, a=sub_items[0], f=f,c=tabState,n=name)
                new_str += snippets[type]['Nav-End'].format(r=randomKey)
        else:
            # Build repeating items
            sub_items = item.split('</h3>')
            print("sub_items: ", sub_items)

            # If there was no </h3>
            if len(sub_items) == 1:
                sub_items.append('')
                new_str = ''


            tabState = ''
            if idx == 1: # If I'm the first item
                tabState = ' active show'
            # rainbow items
            if name == 'Card-Rainbow':
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


    return new_str

def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key