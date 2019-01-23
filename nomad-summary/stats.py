import nomad
from terminaltables import AsciiTable, SingleTable
import click
import re

n = nomad.Nomad()


@click.command()
@click.option('--filter', help='Filter for jobnames (e.g. "production"). Accepts a regex pattern.')
def main(filter):
    jobResourceUsage = dict()

    filterPattern = None
    if filter:
        filterPattern = re.compile(filter)

    with click.progressbar(n.allocations, label="Fetching stats") as allocations:
        for allocation in allocations:
            allocation = n.allocation.get_allocation(allocation["ID"])
            job = allocation["Job"]
            name = job["Name"]
            if filterPattern and not filterPattern.search(name):
                continue

            jobSums = [0, 0]
            for taskgroup in job["TaskGroups"]:
                for task in taskgroup["Tasks"]:
                    resources = task["Resources"]
                    jobSums[0] += resources["CPU"]
                    jobSums[1] += resources["MemoryMB"]

            if name in jobResourceUsage:
                jobResourceUsage[name][0] += jobSums[0]
                jobResourceUsage[name][1] += jobSums[1]
            else:
                jobResourceUsage[name] = jobSums

    print()

    table_data = [
        ["Job Name", "CPU (mhz)", "Memory (MB)"]
    ]

    usages = []
    for key, values in jobResourceUsage.items():
        values.insert(0, key)
        usages.append(values)

    # Sort by memory
    usages = sorted(usages, key=lambda x: x[2], reverse=True)
    table_data.extend(usages)

    table = AsciiTable(table_data, "Resource Usages")
    print(table.table)

    total_memory = 0
    total_cpu = 0

    for usage in usages:
        _, cpu, mem = usage
        total_memory += mem
        total_cpu += cpu

    summary_table_data = [
        ["Memory", f"{total_memory} MB"],
        ["CPU", f"{total_cpu} Mhz"]
    ]

    print()

    table = AsciiTable(summary_table_data, "Total Usage")
    table.inner_heading_row_border = False
    print(table.table)


if __name__ == '__main__':
    main()
