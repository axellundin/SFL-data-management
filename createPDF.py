import sponsor, runner
import session, os

def writeToPDF(SESSION):

    # create folder

    pdfdir = os.getcwd() + "/pdfs/"

    # GET VALID NAME

    name_found = False
    valid_name = SESSION.session_name # As a start 
    
    while not name_found:
        for subdir, dirs, files in os.walk(pdfdir):
            if len(subdir)>len(pdfdir):
                if subdir[len(pdfdir):] == valid_name:
                    valid_name = input(f"The name {valid_name} alredy exists.\nWhat should i save the folder as?\n>")
                    continue
        name_found = True
        
    pdfsessiondir = pdfdir + valid_name

    os.mkdir(pdfsessiondir) 

    # create string with all the information. 

    # write to the file
    # SPONSORS
    with open(os.getcwd() + "/sponsorlist_template", 'r')  as template:
        with open(pdfsessiondir + "/sponsorlist.tex", "w") as texFile:
            for line in template.readlines():
                if '%' in line:
                    for sponsor in SESSION.SPONSORS:
                        sponsor_FN = sponsor.first_name[0].upper() + sponsor.first_name[1:]
                        sponsor_LN = sponsor.last_name[0].upper() + sponsor.last_name[1:]
                        newline =  f"\t\t{sponsor_LN} & {sponsor_FN} & & {sponsor.TO_PAY}" + r"\\" + "\n\t\t" + r"\hline" + "\n"
                        texFile.write(newline) 
                else:
                    texFile.write(line)
    #RUNNERS
    with open(os.getcwd() + "/runnerlist_template", 'r')  as template:
        with open(pdfsessiondir + "/runnerlist.tex", "w") as texFile:
            for line in template.readlines():
                if '%' in line:
                    for runner in SESSION.RUNNERS:
                        runner_FN = runner.first_name[0].upper() + runner.first_name[1:]
                        runner_LN = runner.last_name[0].upper() + runner.last_name[1:]
                        newline = f"\t\t{runner_LN} & {runner_FN} & {runner.number_of_laps} & {runner.collected_in_total}" + r"\\" + "\n\t\t" + r"\hline" + "\n"
                        texFile.write(newline)
                else:
                    texFile.write(line)

    # Compile the PDF FILES

    inputted_path_runners = pdfsessiondir +r"/runnerlist.tex " 
    inputted_path_sponsors = pdfsessiondir +r"/sponsorlist.tex " 
    os.system(f"pdflatex -output-directory={pdfsessiondir} {inputted_path_runners}")
    os.system(f"pdflatex -output-directory={pdfsessiondir} {inputted_path_runne    rs}")

if __name__ == '__main__':
    writeToPDF(2)
