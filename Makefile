DB = experiments.db
PLOTS = tex/time_vs_size.pdf \
		tex/retransmissions_vs_size.pdf \
		tex/retransmissions_vs_size_wo_outliers.pdf \
        tex/time_vs_delay_and_loss_probability.pdf \
        tex/time_vs_delay_and_loss_probability_min_max.pdf \
        tex/retransmissions_vs_delay_and_loss_probability.pdf \
        tex/retransmissions_vs_delay_and_loss_probability_wo_outliers.pdf

.PHONY: all clean new

all: informe.pdf

tex/time_vs_size.pdf: $(DB) src/plot.py src/time_vs_size_plot.py
	./time_vs_size_plot -o tex/time_vs_size.pdf

tex/retransmissions_vs_size.pdf: $(DB) src/plot.py src/retransmissions_vs_size_plot.py
	./retransmissions_vs_size_plot -o tex/retransmissions_vs_size.pdf

tex/retransmissions_vs_size_wo_outliers.pdf: $(DB) src/plot.py src/retransmissions_vs_size_plot.py
	./retransmissions_vs_size_plot --exclude-outliers -o tex/retransmissions_vs_size_wo_outliers.pdf

tex/time_vs_delay_and_loss_probability.pdf: $(DB) src/plot.py src/time_vs_delay_and_loss_probability_plot.py
	./time_vs_delay_and_loss_probability_plot -o tex/time_vs_delay_and_loss_probability.pdf

tex/time_vs_delay_and_loss_probability_min_max.pdf: $(DB) src/plot.py src/time_vs_delay_and_loss_probability_plot.py
	./time_vs_delay_and_loss_probability_plot --only-min-and-max-loss-probabilities -o tex/time_vs_delay_and_loss_probability_min_max.pdf

tex/retransmissions_vs_delay_and_loss_probability.pdf: $(DB) src/plot.py src/retransmissions_vs_delay_and_loss_probability_plot.py
	./retransmissions_vs_delay_and_loss_probability_plot -o tex/retransmissions_vs_delay_and_loss_probability.pdf

tex/retransmissions_vs_delay_and_loss_probability_wo_outliers.pdf: $(DB) src/plot.py src/retransmissions_vs_delay_and_loss_probability_plot.py
	./retransmissions_vs_delay_and_loss_probability_plot --exclude-outliers -o tex/retransmissions_vs_delay_and_loss_probability_wo_outliers.pdf

informe.pdf: tex/informe.tex $(PLOTS)
	cd tex; pdflatex -interaction=nonstopmode -halt-on-error informe.tex && \
	        pdflatex -interaction=nonstopmode -halt-on-error informe.tex
	mv tex/informe.pdf .

clean:
	rm -f informe.pdf tex/*.aux tex/*.log tex/*.toc tex/*.out tex/*.pdf src/*.pyc src/ptc/*.pyc src/test/*.pyc

new: clean all