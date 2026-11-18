import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import assembler
import simulator
from cpu import *

programs = ['p1_add_sub', 'p2_fibonacci', 'p3_reverse_copy', 'p2_fibonacci_opt', 'xor_demo']
main3 = ['p1_add_sub', 'p2_fibonacci', 'p3_reverse_copy']
labels = ['Program 1', 'Program 2', 'Program 3']
colors = ['#4C72B0', '#DD8452', '#55A868']
os.makedirs("graphs", exist_ok=True)

# assemble and run every program, save the traces
results = {}
for p in programs:
    words, data = assembler.assemble(open("programs/" + p + ".asm").readlines())
    assembler.save(p, words, data)
    r = simulator.run("output/" + p + ".hex", M, False)
    open("output/" + p + "_trace.txt", "w").write("\n".join(r['trace']) + "\n")
    results[p] = r
    print(p.ljust(18), "instructions", r['instructions'], " cycles", r['cycles'],
          " CPI", round(r['cpi'], 2), " memory accesses", r['memory_accesses'])

# bar chart: total cycles of the three programs
plt.figure(figsize=(6, 4))
values = [results[p]['cycles'] for p in main3]
plt.bar(labels, values, color=colors)
for i in range(3):
    plt.text(i, values[i] + 1, str(values[i]), ha='center')
plt.title('Total Cycles per Program (M = ' + str(M) + ')')
plt.ylabel('Cycles')
plt.tight_layout()
plt.savefig("graphs/cycles_per_program.png", dpi=200)
plt.close()

# bar chart: original vs optimized program 2
plt.figure(figsize=(6, 4))
values = [results['p2_fibonacci']['cycles'], results['p2_fibonacci_opt']['cycles']]
plt.bar(['Program 2 (original)', 'Program 2 (with LOOP)'], values, color=['#4C72B0', '#55A868'])
for i in range(2):
    plt.text(i, values[i] + 0.5, str(values[i]), ha='center')
plt.title('Original vs Optimized')
plt.ylabel('Cycles')
plt.tight_layout()
plt.savefig("graphs/original_vs_optimized.png", dpi=200)
plt.close()

# pie charts: instruction mix
fig, axes = plt.subplots(1, 3, figsize=(14, 5.2))
for i in range(3):
    mix = results[main3[i]]['mix']
    keys = list(mix.keys())
    wedges, t1, t2 = axes[i].pie(list(mix.values()), autopct=lambda v: str(round(v)) + '%' if v >= 5 else '',
                                 startangle=90, pctdistance=0.75, colors=plt.cm.tab20.colors)
    axes[i].legend(wedges, [k + " (" + str(mix[k]) + ")" for k in keys], loc='upper center',
                   bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=9, frameon=False)
    axes[i].set_title(labels[i] + ' (' + str(results[main3[i]]['instructions']) + ' instructions)')
plt.suptitle('Instruction Mix', fontsize=14)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("graphs/instruction_mix.png", dpi=200)
plt.close()

# line graph: total cycles when M goes from 1 to 5
plt.figure(figsize=(6, 4))
for i in range(3):
    ys = []
    for m in range(1, 6):
        ys.append(simulator.run("output/" + main3[i] + ".hex", m, False)['cycles'])
    print(labels[i], "cycles for M = 1..5:", ys)
    plt.plot(range(1, 6), ys, marker='o', label=labels[i], color=colors[i])
plt.xticks(range(1, 6))
plt.xlabel('Memory cost M (cycles)')
plt.ylabel('Total cycles')
plt.title('Effect of Memory Speed')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("graphs/memory_cost.png", dpi=200)
plt.close()
