#PBS -l nodes=1:ppn=1
#PBS -l walltime=6:00:00
#PBS -j oe
#PBS -l pmem=16gb

cd $PBS_O_WORKDIR

echo " "
echo " "
echo "Job started on `hostname` at `date`"
echo " "

module load mothur
#
#
#mothur "#set.logfile(name=01_Oil_DNA.mothur.make_contigs_subsample_summary.logfile); make.contigs(file=Oil_DNA.txt, processors=1); sub.sample(fasta=Oil_DNA.trim.contigs.fasta, group=Oil_DNA.contigs.groups, size=300000); summary.seqs()"
#mothur "#set.logfile(name=02_Oil_DNA.mothur.screen_unique_count.logfile);  screen.seqs(fasta=Oil_DNA.trim.contigs.subsample.fasta, group=Oil_DNA.contigs.subsample.groups, maxambig=0, minlength=290, maxlength=295, maxhomop=8); summary.seqs(); unique.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.fasta); count.seqs(name=Oil_DNA.trim.contigs.subsample.good.names, group=Oil_DNA.contigs.subsample.good.groups); summary.seqs(count=Oil_DNA.trim.contigs.subsample.good.count_table)"
#mothur "#pcr.seqs(fasta=~/scratch/silva.nr_v128.align, start=11894, end=25319, keepdots=F, processors=1)"
#mothur "#set.logfile(name=03_Oil_DNA.mothur.align.logfile); align.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.fasta, reference=~/scratch/silva.nr_v128.pcr.align, flip=t); summary.seqs(fasta=current, count=Oil_DNA.trim.contigs.subsample.good.count_table)"
#mothur "#set.logfile(name=04_Oil_DNA.mothur.screen_filter.logfile); screen.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.align, count=Oil_DNA.trim.contigs.subsample.good.count_table, summary=Oil_DNA.trim.contigs.subsample.good.unique.summary, start=1, end=13424); summary.seqs(fasta=current, count=current); filter.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.align, vertical=T, trump=.)"
#mothur "#set.logfile(name=05_Oil_DNA.mothur.unique_summary.logfile); unique.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.fasta, count=Oil_DNA.trim.contigs.subsample.good.good.count_table); summary.seqs(fasta=current, count=current)"
#mothur "#set.logfile(name=06_Oil_DNA.mothur.precluster_summary.logfile); pre.cluster(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.fasta, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.count_table, diffs=2); summary.seqs(fasta=current, count=current)"
#mothur "#set.logfile(name=07_Oil_DNA.mothur.chimera_remove_summary.logfile); chimera.uchime(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.fasta, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.count_table, dereplicate=t); remove.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.fasta, accnos=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.accnos); summary.seqs(fasta=current, count=current)"
#mothur "#set.logfile(name=08_Oil_DNA.mothur.classify.logfile); classify.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.fasta, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.pick.count_table, reference=~/scratch/silva.nr_v128.align, taxonomy=~/scratch/silva.nr_v128.tax, cutoff=80, processors=1)" 
#mothur "#set.logfile(name=09_Oil_DNA.mothur.remove_summary.logfile); remove.lineage(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.fasta, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.pick.count_table, taxonomy=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.nr_v128.wang.taxonomy, taxon=Chloroplast-Mitochondria-unknown); summary.seqs(fasta=current, count=current)"
#mothur "#set.logfile(name=10a_Oil_DNA.mothur.dist.logfile); dist.seqs(fasta=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.pick.fasta, cutoff=0.10, processors=4)"
#mothur "#set.logfile(name=10b_Oil_DNA.mothur.cluster.logfile); cluster(column=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.pick.dist, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.pick.pick.count_table)"
#mothur "#set.logfile(name=11_Oil_DNA.mothur.makeshared.logfile); make.shared(list=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.list, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.pick.pick.count_table)"
mothur "#set.logfile(name=12_Oil_DNA.mothur.classify_otu.logfile); classify.otu(list=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.list, count=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.uchime.pick.pick.count_table, taxonomy=Oil_DNA.trim.contigs.subsample.good.unique.good.filter.unique.precluster.pick.nr_v128.wang.taxonomy)"


echo " "

echo "Job Ended on `hostname` at `date`"
echo " "

