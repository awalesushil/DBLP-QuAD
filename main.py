import argparse
import logging

from models import DataGenerator, ParaphrasePairGenerator
from utils import save_to_json, save_paraphrases_json
from utils import plot_question_distributions, plot_template_distribution
from utils import index_graph, load_graph


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--index", action="store_true", help="Index the graph")
    parser.add_argument("--graph_path", type=str, default="data/dblp.nt", help="Path to the graph")

    parser.add_argument("--generate", action="store_true", help="Generate data")
    parser.add_argument("--size", type=int, default=10000, help="Number of questions to generate")
    parser.add_argument("--seed", type=int, default=2358, help="Random seed")

    parser.add_argument("--generate_paraphrases", action="store_true", help="Generate paraphrases")

    parser.add_argument("--stats", action="store_true", help="Show stats")
    
    args = parser.parse_args()

    if args.index:
        index_graph(args.graph_path)
    
    if args.generate:

        graph = load_graph()
        dataGenerator = DataGenerator(graph, args.seed)
        
        data_size = {
            "train": int(args.size * 0.7),
            "valid": int(args.size * 0.1),
            "test": int(args.size * 0.2)
        }
        
        for group, size in data_size.items():
            logging.info(f"Generating {size} {group} questions")
            generator = dataGenerator.generate(group, size)
            save_to_json(group+"_questions.json", group+"_answers.json", "failed_queries.json", generator)
    
    if args.generate_paraphrases:
        logging.info("Generating paraphrases")
        graph = load_graph()
        paraphraseGenerator = ParaphrasePairGenerator(graph, args.seed)
        generator = paraphraseGenerator.generate()
        save_paraphrases_json("paraphrase_pairs.json", generator=generator)

    if args.stats:
        plot_template_distribution()
        plot_question_distributions()

