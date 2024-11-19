<h3>Instructions for running <code>crawler.py</code></h3>

<h5>Activate the environment</h5> 
In the <code>~/cs3640</code> directory, run <code>source ~/cs3640/A3/bin/activate</code>

<h5>Install dependencies</h5> 

<strong>Installing PoliPy</strong> <br>
Install PoliPy with <code>pip install polipy</code>

<strong>Installing FireFox Browser</strong> <br>
Install Mozilla Firefox Browser for Ubuntu with <code>sudo apt install firefox -y</code>. You can verify installation with <code>firefox --version</code>. <br><br>

Navigate to the <code>~/cs3640/A5</code> directory <br><br>

<strong>Installing Geckodeck driver</strong> <br>
Download the correct Geckodeck driver for your machine [here](https://github.com/mozilla/geckodriver/releases) 
and add the .tar.gz file to the A5 directory. <br>
Install the Geckodeck driver with <code>tar -xvzf geckodriver-*.tar.gz</code>. <br>
Move the GeckoDeck driver to the desired path with <code>sudo mv geckodriver /usr/local/bin/</code>. You can verify installation with <code>which geckodriver</code>


<h5>Run Crawler.py</h5> 
Navigate to the <code>~/cs3640/A5/crawler</code> directory <br>