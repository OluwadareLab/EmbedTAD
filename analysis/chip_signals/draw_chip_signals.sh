# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/gm12878/gse63525_gm12878_5000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/gm12878_5000_chr19.h5 --chromosome 19 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/gm12878/gse63525_gm12878_10000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/gm12878_10000_chr19.h5 --chromosome 19 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/gm12878/gse63525_gm12878_5000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/gm12878_5000_chr3.h5 --chromosome 3 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/gm12878/gse63525_gm12878_10000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/gm12878_10000_chr3.h5 --chromosome 3 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/ch12lx/ch12lx_5000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/ch12lx_5000_chr2.h5 --chromosome chr2 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/ch12lx/ch12lx_10000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/ch12lx_10000_chr2.h5 --chromosome chr2 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/ch12lx/ch12lx_5000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/ch12lx_5000_chr18.h5 --chromosome chr18 &
# hicConvertFormat -m /home/mohit/Documents/project/embed_tad/data/raw/ch12lx/ch12lx_10000.cool --inputFormat cool --outputFormat h5 -o /home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/chip_signals/ch12lx_10000_chr18.h5 --chromosome chr18 &
# wait

# awk -F"\t" '{print "chr3\t" $1*5000 "\t" $2*5000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/gm12878/gm12878_5000_chr3.txt > gm12878_5000_chr3_embedtad.bed &
# awk -F"\t" '{print "chr3\t" $1*10000 "\t" $2*10000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/gm12878/gm12878_10000_chr3.txt > gm12878_10000_chr3_embedtad.bed &
# awk -F"\t" '{print "chr19\t" $1*5000 "\t" $2*5000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/gm12878/gm12878_5000_chr19.txt > gm12878_5000_chr19_embedtad.bed &
# awk -F"\t" '{print "chr19\t" $1*10000 "\t" $2*10000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/gm12878/gm12878_10000_chr19.txt > gm12878_10000_chr19_embedtad.bed &
# awk -F"\t" '{print "chr2\t" $1*5000 "\t" $2*5000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/ch12lx/ch12lx_5000_chr2.txt > ch12lx_5000_chr2_embedtad.bed &
# awk -F"\t" '{print "chr2\t" $1*10000 "\t" $2*10000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/ch12lx/ch12lx_10000_chr2.txt > ch12lx_10000_chr2_embedtad.bed &
# awk -F"\t" '{print "chr18\t" $1*5000 "\t" $2*5000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/ch12lx/ch12lx_5000_chr18.txt > ch12lx_5000_chr18_embedtad.bed &
# awk -F"\t" '{print "chr18\t" $1*10000 "\t" $2*10000}' /home/mohit/Documents/project/embed_tad/data/results/gpu/ch12lx/ch12lx_10000_chr18.txt > ch12lx_10000_chr18_embedtad.bed &
# wait

# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_ctcf.bigwig ch12lx_ctcf.bw &   
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_h3k27ac.bigwig ch12lx_h3k27ac.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_h3k27me3.bigwig ch12lx_h3k27me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_h3k4me1.bigwig ch12lx_h3k4me1.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_h3k4me3.bigwig ch12lx_h3k4me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_h3k9me3.bigwig ch12lx_h3k9me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_rad21.bigwig ch12lx_rad21.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/ch12lx_smc3.bigwig ch12lx_smc3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_ctcf.bigwig gm12878_ctcf.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_h3k27ac.bigwig gm12878_h3k27ac.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_h3k27me3.bigwig gm12878_h3k27me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_h3k4me1.bigwig gm12878_h3k4me1.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_h3k4me3.bigwig gm12878_h3k4me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_h3k9me3.bigwig gm12878_h3k9me3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_rad21.bigwig gm12878_rad21.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/gm12878_smc3.bigwig gm12878_smc3.bw &
# cp /home/mohit/Documents/project/embed_tad/data/raw/chip_signals/mESC_h3k4me3.bigwig mESC_h3k4me3.bw &
# wait
 
# cp gm12878_10000_chr19.ini gm12878_10000_chr3.ini &
# cp gm12878_5000_chr19.ini gm12878_5000_chr3.ini &
# cp gm12878_10000_chr19.ini ch12lx_10000_chr2.ini &
# cp gm12878_5000_chr19.ini ch12lx_5000_chr2.ini &
# cp gm12878_10000_chr19.ini ch12lx_10000_chr18.ini &
# cp gm12878_5000_chr19.ini ch12lx_5000_chr18.ini &
# wait


# pyGenomeTracks --tracks gm12878_5000_chr3.ini --region chr3:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_gm12878_5000_chr3.png &
# pyGenomeTracks --tracks gm12878_10000_chr3.ini --region chr3:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_gm12878_10000_chr3.png &
# pyGenomeTracks --tracks gm12878_5000_chr19.ini --region chr19:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_gm12878_5000_chr19.png &
# pyGenomeTracks --tracks gm12878_10000_chr19.ini --region chr19:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_gm12878_10000_chr19.png &

# pyGenomeTracks --tracks ch12lx_5000_chr2.ini --region chr2:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_ch12lx_5000_chr2.png &
# pyGenomeTracks --tracks ch12lx_10000_chr2.ini --region chr2:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_ch12lx_10000_chr2.png &
# pyGenomeTracks --tracks ch12lx_5000_chr18.ini --region chr18:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_ch12lx_5000_chr18.png &
# pyGenomeTracks --tracks ch12lx_10000_chr18.ini --region chr18:50000000-54000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_ch12lx_10000_chr18.png &
# wait

# cp /home/mohit/Documents/project/embed_tad/data/raw/mesc_gse35156/mesc_40000_chr1.h5 mesc_40000_chr1.h5 &
# cp /home/mohit/Documents/project/embed_tad/data/raw/mesc_gse35156/mesc_40000_chr3.h5 mesc_40000_chr3.h5 &
# cp /home/mohit/Documents/project/embed_tad/data/raw/mesc_gse35156/mesc_40000_chr17.h5 mesc_40000_chr17.h5 &
# cp /home/mohit/Documents/project/embed_tad/data/raw/mesc_gse35156/mesc_40000_chr19.h5 mesc_40000_chr19.h5 &
# wait
# awk -F"\t" '{print "chr1\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mesc_gse35156/mesc_ori_40000_chr1.txt > mesc_40000_chr1.bed &
# awk -F"\t" '{print "chr3\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mesc_gse35156/mesc_ori_40000_chr3.txt > mesc_40000_chr3.bed &
# awk -F"\t" '{print "chr17\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mesc_gse35156/mesc_ori_40000_chr17.txt > mesc_40000_chr17.bed &
# awk -F"\t" '{print "chr19\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mesc_gse35156/mesc_ori_40000_chr19.txt > mesc_40000_chr19.bed &
# wait

# awk -F"\t" '{print $1 "\t" $2 "\t" $3}' /home/mohit/Documents/project/HPTAD/data/result/foo.HPTAD.chr1.40000.tads.bed > mesc_hptad_40000_chr1.bed &
# awk -F"\t" '{print $1 "\t" $2 "\t" $3}' /home/mohit/Documents/project/HPTAD/data/result/foo.HPTAD.chr3.40000.tads.bed > mesc_hptad_40000_chr3.bed &
# awk -F"\t" '{print $1 "\t" $2 "\t" $3}' /home/mohit/Documents/project/HPTAD/data/result/foo.HPTAD.chr17.40000.tads.bed > mesc_hptad_40000_chr17.bed &
# awk -F"\t" '{print $1 "\t" $2 "\t" $3}' /home/mohit/Documents/project/HPTAD/data/result/foo.HPTAD.chr19.40000.tads.bed > mesc_hptad_40000_chr19.bed &
# wait

# pyGenomeTracks --tracks mesc_40000_chr1.ini --region chr1:20000000-26000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mesc_40000_chr1.png &
# pyGenomeTracks --tracks mesc_40000_chr3.ini --region chr3:20000000-26000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mesc_40000_chr3.png &
# pyGenomeTracks --tracks mesc_40000_chr17.ini --region chr17:20000000-26000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mesc_40000_chr17.png &
# pyGenomeTracks --tracks mesc_40000_chr19.ini --region chr19:20000000-26000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mesc_40000_chr19.png &
# wait

# cp /home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/naive_10000.h5 naive_10000.h5 &
# cp /home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/th17_10000.h5 th17_10000.h5 &
# cp /home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/th1_10000.h5 th1_10000.h5 &
# awk -F"\t" '{print "chr2\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr2.txt > naive_10000_chr2.bed &
# awk -F"\t" '{print "chr2\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr2.txt > th17_10000_chr2.bed &
# awk -F"\t" '{print "chr2\t" $1 "\t" $2}' /home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr2.txt > th1_10000_chr2.bed &
# wait

# pyGenomeTracks --tracks mus_10000_chr2_naive_th17.ini --region chr2:28000000-32000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mus_10000_chr2_naive_th17.png &
# pyGenomeTracks --tracks mus_10000_chr2_naive_th1.ini --region chr2:36000000-40000000 --width 40 --dpi 600 -out /home/mohit/Documents/project/embed_tad/plots/chip_sig_mus_10000_chr2_naive_th1.png &
# wait