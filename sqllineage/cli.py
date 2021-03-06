import argparse
import logging

from sqllineage.drawing import draw_lineage_graph
from sqllineage.helpers import extract_sql_from_args
from sqllineage.runner import LineageRunner

logger = logging.getLogger(__name__)


def main(args=None) -> None:
    """
    The command line interface entry point.

    :param args: the command line arguments for sqllineage command
    """
    parser = argparse.ArgumentParser(
        prog="sqllineage", description="SQL Lineage Parser."
    )
    parser.add_argument(
        "-e", metavar="<quoted-query-string>", help="SQL from command line"
    )
    parser.add_argument("-f", metavar="<filename>", help="SQL from files")
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity, show statement level lineage result",
        action="store_true",
    )
    parser.add_argument(
        "-g",
        "--graph-visualization",
        help="show graph visualization of the lineage within a webserver",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        help="the port visualization webserver will be listening on",
        type=int,
        default=5000,
        metavar="<port_number>{0..65536}",
    )
    args = parser.parse_args(args)
    if args.e and args.f:
        logging.warning(
            "Both -e and -f options are specified. -e option will be ignored"
        )
    if args.f or args.e:
        if args.graph_visualization:
            draw_lineage_graph(**args.__dict__)
        else:
            sql = extract_sql_from_args(args)
            runner = LineageRunner(sql, verbose=args.verbose)
            print(runner)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
