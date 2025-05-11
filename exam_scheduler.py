import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import logging

class ExamScheduler:
    """
    Class that handles exam scheduling using graph coloring algorithm
    """
    
    def __init__(self, subjects, students):
        """
        Initialize the exam scheduler
        
        Args:
            subjects (list): List of subject names
            students (dict): Dictionary mapping student names to lists of subjects they are enrolled in
        """
        self.subjects = subjects
        self.students = students
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """
        Build a graph where nodes are subjects and edges represent conflicts
        (subjects that share at least one student)
        
        Returns:
            nx.Graph: The constructed graph
        """
        # Create an empty graph
        G = nx.Graph()
        
        # Add subjects as nodes
        for subject in self.subjects:
            G.add_node(subject)
        
        # Create a dictionary to track which students are enrolled in each subject
        subject_students = {subject: [] for subject in self.subjects}
        
        # Populate the subject_students dictionary
        for student, enrolled_subjects in self.students.items():
            for subject in enrolled_subjects:
                if subject in self.subjects:  # Make sure the subject is valid
                    subject_students[subject].append(student)
        
        # Add edges between subjects that share at least one student
        for i, subject1 in enumerate(self.subjects):
            for subject2 in self.subjects[i+1:]:
                # Check if there's any student enrolled in both subjects
                if any(student in subject_students[subject2] for student in subject_students[subject1]):
                    G.add_edge(subject1, subject2)
        
        return G
    
    def generate_schedule(self):
        """
        Generate an exam schedule using graph coloring algorithm
        
        Returns:
            dict: A dictionary mapping subjects to time slots
        """
        # Use the greedy coloring algorithm
        coloring = self._greedy_coloring()
        
        # The coloring is our schedule (color = time slot)
        return coloring
    
    def _greedy_coloring(self):
        """
        Implement the greedy graph coloring algorithm
        
        Returns:
            dict: A dictionary mapping nodes (subjects) to colors (time slots)
        """
        # Sort nodes by degree (number of conflicts) in descending order
        # This is a common heuristic that often gives better results
        nodes = sorted(self.graph.nodes(), key=lambda x: self.graph.degree(x), reverse=True)
        
        # Initialize the colors dictionary
        colors = {}
        
        # Iterate through each node
        for node in nodes:
            # Get the colors of all neighbors
            neighbor_colors = {colors[neighbor] for neighbor in self.graph.neighbors(node)
                              if neighbor in colors}
            
            # Find the first available color that is not used by any neighbor
            color = 1
            while color in neighbor_colors:
                color += 1
            
            # Assign the color to the node
            colors[node] = color
        
        return colors
    
    def visualize_graph(self):
        """
        Visualize the graph with nodes colored according to the schedule
        
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        # Get the coloring (schedule)
        coloring = self.generate_schedule()
        
        # Create a new figure
        plt.figure(figsize=(10, 8))
        
        # Use a fixed position layout for consistent results
        pos = nx.spring_layout(self.graph, seed=42)
        
        # Define a list of distinct colors for visualization
        color_map = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # Map time slots to colors for visualization
        node_colors = [color_map[(coloring[node] - 1) % len(color_map)] for node in self.graph.nodes()]
        
        # Draw the graph
        nx.draw_networkx(
            self.graph, 
            pos=pos, 
            node_color=node_colors,
            node_size=500, 
            font_size=10,
            font_weight='bold',
            width=2,
            edge_color='gray',
            with_labels=True
        )
        
        # Create a legend for time slots
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[(slot - 1) % len(color_map)], 
                  markersize=10, label=f'Time Slot {slot}')
            for slot in sorted(set(coloring.values()))
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # Set the title and remove the axes
        plt.title('Exam Schedule Graph Coloring')
        plt.axis('off')
        
        # Return the figure for further processing
        return plt.gcf()

# Example usage if the file is run directly
if __name__ == "__main__":
    subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
    students = {
        'Alice': ['Math', 'Physics', 'English'],
        'Bob': ['Math', 'Chemistry'],
        'Charlie': ['Physics', 'Biology'],
        'Daisy': ['Math', 'English', 'Biology'],
        'Eve': ['Chemistry', 'Biology']
    }
    
    scheduler = ExamScheduler(subjects, students)
    schedule = scheduler.generate_schedule()
    
    print("Exam Schedule:")
    for subject, time_slot in schedule.items():
        print(f"{subject}: Time Slot {time_slot}")
    
    # Visualize the graph
    scheduler.visualize_graph()
    plt.savefig('exam_schedule_graph.png')
