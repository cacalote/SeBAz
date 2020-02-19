# returns a list f benchmarks that matchess the options
def get_recommendations(options):

    if options.dist == 'ind':
        from modules.benchmarks import benchmark_ind as benchmark
    elif options.dist == 'cen':
        from modules.benchmarks import benchmark_cen as benchmark
    elif options.dist == 'deb':
        from modules.benchmarks import benchmark_deb as benchmark
    elif options.dist == 'fed':
        from modules.benchmarks import benchmark_fed as benchmark
    elif options.dist == 'red':
        from modules.benchmarks import benchmark_red as benchmark
    elif options.dist == 'sus':
        from modules.benchmarks import benchmark_sus as benchmark
    elif options.dist == 'ubu':
        from modules.benchmarks import benchmark_ubu as benchmark

    recommendations = list()

    # to weed out scored / not scored recommendations
    if options.score != None:
        recommendations = [b for b in benchmark if b[1] == options.score]

    # to weed out recommendations based on platform
    if options.platform:
        if options.platform == 'server':
            platform = [b for b in benchmark if 1 == b[3] or 3 == b[3]]
        else:
            platform = [b for b in benchmark if 2 == b[3] or 3 == b[3]]
        if recommendations:
            recommendations = [p for p in platform if p in recommendations]
        else:
            recommendations = platform

    # to weed out recommendations based on Profile Level
    if options.level:
        level = [b for b in benchmark if b[2] == options.level]
        if recommendations:
            recommendations = [l for l in level if l in recommendations]
        else:
            recommendations = level

    import re

    # to select (whitelist) recommendations based on option
    if options.include:
        include = list()
        for i in options.include:
            r = re.compile(i)
            include.extend(list(filter(r.match, [b[0] for b in benchmark])))
        if not include:
            if all(i.startswith(('1', '2', '3', '4', '5', '6')) for i in options.include):
                exit('Could not perform benchmarks on ' +
                     ' '.join(options.include) + ' with given conditions. Exiting.')
            else:
                exit('Can\'t inlcude recommendations not defined in CIS Benchmark document.\nRun -h/--help or refer to the documentation.')
        elif recommendations:
            recommendations = [r for r in recommendations if r[0] in include]
        else:
            recommendations = [b for b in benchmark if b[0] in include]

    # to remove (blacklist) recommendations based on option
    if options.exclude:
        exclude = list()
        for e in options.exclude:
            r = re.compile(e)
            exclude.extend(list(filter(r.match, [b[0] for b in benchmark])))
        if recommendations:
            recommendations = [r for r in recommendations if r[0] not in exclude]
        else:
            recommendations = [b for b in benchmark if b[0] not in exclude]

    if not recommendations and options.score == None and not options.platform and not options.level and not options.include and not options.exclude:
        recommendations = [b for b in benchmark]

    # returning the requested recommendations
    return recommendations


# displays the explaination necessary recommendations and exits
def disp_exp(options):

    if options.dist == 'ind':
        from modules.benchmarks import benchmark_ind as benchmark
    elif options.dist == 'cen':
        from modules.benchmarks import benchmark_cen as benchmark
    elif options.dist == 'deb':
        from modules.benchmarks import benchmark_deb as benchmark
    elif options.dist == 'fed':
        from modules.benchmarks import benchmark_fed as benchmark
    elif options.dist == 'red':
        from modules.benchmarks import benchmark_red as benchmark
    elif options.dist == 'sus':
        from modules.benchmarks import benchmark_sus as benchmark
    elif options.dist == 'ubu':
        from modules.benchmarks import benchmark_ubu as benchmark

    recommendations = list()
    include = list()
    exp = list()

    import re

    for i in options.exp:
        r = re.compile(i)
        include.extend(list(filter(r.match, [b[0] for b in benchmark])))
    exp = [b for b in benchmark if b[0] in include]
    for b in exp:
        result = b[0] + '\t' + b[4] + '\t'
        result += 'Scored\t' if b[1] else 'Not Scored\t'
        result += 'Level 1\t' if b[2] == 1 else 'Level 2\t'
        if b[3] == 1:
            result += 'Server'
        elif b[3] == 2:
            result += 'Workstation'
        else:
            result += 'Both S and W'
        print(result)
    exit()