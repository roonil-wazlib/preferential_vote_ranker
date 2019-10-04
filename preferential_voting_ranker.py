from tkinter import *
from tkinter import ttk
from matplotlib import pyplot

#change these categories to the options you care about
ranking_categories = ["Environment", "Economics", "Values", "Likeability"]
candidate_objects = []

class GUI:
    
    def __init__(self, master, candidates):
        self.master = master
        self.ranking_frame = Frame(master)
        self.ranking_frame.pack()
        self.candidates = candidates
        self.current = 0
        self.values = [1] + list(range(1,11))
        
        self.name_label = ttk.Label(self.ranking_frame, text=candidates[self.current], font=('Helvetica', 18, 'bold'))
        self.name_label.grid(row=0,column=0,columnspan=2, padx=5,pady=5)
        
        self.submit = ttk.Button(self.ranking_frame, text="Save", command=self.store_candidate_values)
        self.submit.grid(row=len(ranking_categories)+1, column=0, columnspan=2, pady=10)
        
        self.set_up_buttons()
        
        
    def set_up_buttons(self):
        
        self.ranking_labels = []
        self.ranking_optionmenues = []
        self.scores = []
        
        for index, ranker in enumerate(ranking_categories):
            self.ranking_labels.append(ttk.Label(self.ranking_frame, text=ranker))
            self.ranking_labels[-1].grid(row=index+1, column=0, padx=10,pady=5)
            
            self.scores.append(StringVar(self.master))
            
            self.ranking_optionmenues.append(ttk.OptionMenu(self.ranking_frame, self.scores[-1], *self.values))
            self.ranking_optionmenues[-1].grid(row=index+1, column=1,padx=10,pady=5)        
        
        
    def store_candidate_values(self):
        raw_scores = [int(x.get()) for x in self.scores]
        candidate_objects.append(Candidate(self.candidates[self.current], raw_scores, self.current))
        
        self.update_candidate()
        
        
    def update_candidate(self):
        self.current += 1
        if self.current >= len(self.candidates):
            self.ranking_frame.destroy()
            self.make_graph_options()
            self.display_overall_results()
            
        else:
            self.name_label.config(text=candidates[self.current])
            self.set_up_buttons()
            
            
    def make_graph_options(self):
        ttk.Label(self.master, text="Filter by:").pack()
        
        options = ["Total", "Total"] + ranking_categories
        self.graph = StringVar(self.master)
        graph_selection = ttk.OptionMenu(self.master, self.graph, *options, command=self.change_graph)
        graph_selection.pack()
        
    
    def change_graph(self, selection):
        graph_type = -1
        for index, item in enumerate(ranking_categories):
            if selection == item:
                graph_type = index
        if graph_type == -1:
            self.display_overall_results()
        else:
            self.display_filtered_results(graph_type)
            
            
    def display_overall_results(self):
        sorted_candidate_objects = sorted(candidate_objects, reverse=True, key=lambda x: sum(x.scores))
        names = [x.name.split(' ')[-1][:4] for x in sorted_candidate_objects]
        totals = [sum(x.scores) for x in sorted_candidate_objects]
        
        print("\n\nTOTALS:\n")
        for index, item in enumerate(sorted_candidate_objects):
            print("{}: {} with a total of {}".format(index+1, item.name, sum(item.scores)))
        #print([(x.name, sum(x.scores)) for x in sorted_candidate_objects])
        
        make_graph(names[:10], totals[:10], "Total")
        
        
    def display_filtered_results(self, index):
        sorted_candidate_objects = sorted(candidate_objects, reverse=True, key=lambda x: x.scores[index])
        names = [x.name.split(' ')[-1][:4] for x in sorted_candidate_objects]
        totals = [x.scores[index] for x in sorted_candidate_objects]
        
        print("\n\n" + ranking_categories[index] + ":\n")
        for location, item in enumerate(sorted_candidate_objects):
            print("{}: {} with a total of {}".format(location+1, item.name, item.scores[index]))
        #print([(x.name, sum(x.scores)) for x in sorted_candidate_objects])
        
        make_graph(names[:10], totals[:10], ranking_categories[index])   
        
  
  

class Candidate:
    def __init__(self, name, scores, ID):
        self.name = name
        self.scores = scores
        self.ID = ID
    
    


def load_file(file_name):
    with open(file_name) as infile:
        candidates = infile.read().splitlines()
    return candidates


def make_graph(x_list, y_list, category):
    pyplot.figure(figsize=(8,8))
    pyplot.bar(x_list, y_list, align='center', alpha=0.5)
    pyplot.title("{} Results for Top 10 Candidates".format(category))
    pyplot.xlabel('Candidate')
    pyplot.ylabel('Total')
    pyplot.show()


if __name__ == '__main__':
    
    candidates = load_file("candidates_list.txt") #candidates for 2019 Christchurch general election
    
    root = Tk()
    root.geometry("500x500")
    gui = GUI(root, candidates)
    root.mainloop()