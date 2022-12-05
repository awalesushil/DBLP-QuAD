import argparse
import logging

from models import DataGenerator
from utils import save_to_json
from utils import plot_question_distributions, plot_template_distribution
from utils import index_graph, load_graph


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--index", action="store_true", help="Index the graph")
    parser.add_argument("--graph_path", type=str, default="data/dblp.nt", help="Path to the graph")

    parser.add_argument("--generate", action="store_true", help="Generate data")
    parser.add_argument("--data_file", type=str, default="data.json", help="Data file name")
    parser.add_argument("--failed_queries_file", type=str, default="failed_queries.json", help="Failed queries file name")
    parser.add_argument("--answers_file", type=str, default="answers.json", help="Answers file name")
    parser.add_argument("--size", type=int, default=5000, help="Number of questions to generate")
    parser.add_argument("--seed", type=int, default=2358, help="Random seed")

    parser.add_argument("--stats", action="store_true", help="Show stats")
    
    args = parser.parse_args()

    if args.index:
        index_graph(args.graph_path)
    
    if args.generate:
        graph = load_graph()
        dataGenerator = DataGenerator(graph, args.seed)
        generator = dataGenerator.generate(args.size)
        save_to_json(args.data_file, args.answers_file, args.failed_queries_file, generator)
    
    if args.stats:
        plot_template_distribution()
        plot_question_distributions()

