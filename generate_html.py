import json

with open("stock_data.json", "r") as f:
    data = json.load(f)

# we will inject this data into a JS string in the HTML.
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Return Calculator: Total Return with Dividends Reinvested | FireMaths</title>
    <meta name="description" content="Think you know how much your AAPL stock really made? The true stock return calculator reveals the massive hidden impact of reinvested dividends on total returns.">
    <link rel="canonical" href="https://firemaths.info/stock-return-calculator.html">
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-G86C7NJG3F"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-G86C7NJG3F');</script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg: #060a12;
            --card-bg: #0a1020;
            --border: #152040;
            --accent: #D4A017;
            --text: #e0e6ed;
            --text-muted: #8a9bb2;
            --danger: #ff4a4a;
            --success: #4aff8a;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: var(--font-body);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        .sticky-nav {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(6, 10, 18, 0.85);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sticky-nav .brand {
            font-weight: 800;
            font-size: 1.25rem;
            color: var(--accent);
            text-decoration: none;
        }

        .sticky-nav .links a {
            color: var(--text);
            text-decoration: none;
            margin-left: 1.5rem;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }

        .sticky-nav .links a:hover {
            color: var(--accent);
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
        }

        h1, h2, h3 { line-height: 1.2; font-weight: 700; }

        header { text-align: center; margin-bottom: 3rem; }
        header h1 { font-size: 2.5rem; color: var(--accent); margin-bottom: 1rem; }
        header p { color: var(--text-muted); font-size: 1.1rem; }

        .dashboard {
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }
        @media(min-width: 768px) {
            .dashboard { grid-template-columns: 1fr 1fr; }
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }

        .card h2 {
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .input-group { margin-bottom: 1.5rem; }
        .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        select, input {
            width: 100%;
            background: var(--bg);
            border: 1px solid var(--border);
            color: var(--text);
            font-family: var(--font-mono);
            padding: 0.75rem;
            border-radius: 6px;
            font-size: 1rem;
        }

        select:focus, input:focus {
            outline: none;
            border-color: var(--accent);
        }

        .btn {
            display: block;
            width: 100%;
            background: var(--accent);
            color: #000;
            border: none;
            padding: 1rem;
            font-size: 1rem;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            transition: opacity 0.2s;
            margin-top: 1rem;
        }
        .btn:hover { opacity: 0.9; }

        .result-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px dashed var(--border);
        }
        .result-item:last-child { border-bottom: none; }
        .result-label { font-size: 0.9rem; color: var(--text-muted); }
        .result-val { font-family: var(--font-mono); font-size: 1.25rem; font-weight: 600; }

        .val-pos { color: var(--success); }
        .val-neg { color: var(--danger); }
        .val-neutral { color: var(--text); }

        .chart-container {
            width: 100%;
            height: 300px;
            margin-top: 2rem;
            position: relative;
        }

        canvas {
            width: 100%;
            height: 100%;
        }

        .faq-section {
            margin-top: 4rem;
        }
        .faq-section h2 { margin-bottom: 2rem; color: var(--accent); }
        .faq-item {
            margin-bottom: 1.5rem;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
        }
        .faq-item h3 { font-size: 1.1rem; margin-bottom: 0.75rem; }
        .faq-item p { color: var(--text-muted); }

        footer {
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .copy-btn {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 0.2rem 0.5rem;
            font-size: 0.75rem;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 0.5rem;
        }
        .copy-btn:hover { color: var(--text); border-color: var(--accent); }
    </style>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Stock Return Calculator: Total Return with Dividends Reinvested",
      "description": "Think you know how much your AAPL stock really made? The true stock return calculator reveals the massive hidden impact of reinvested dividends on total returns.",
      "datePublished": "2026-03-11",
      "publisher": {
        "@type": "Organization",
        "name": "FireMaths",
        "logo": {
          "@type": "ImageObject",
          "url": "https://firemaths.info/favicon.ico"
        }
      }
    }
    </script>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How does a stock return calculator work?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A stock return calculator computes the total return on an investment by taking the difference between the buy and sell prices, adding any accumulated dividends, and comparing it to the initial amount invested."
          }
        },
        {
          "@type": "Question",
          "name": "Why is a total return calculator with dividends important?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Using a total return calculator with dividends gives a more accurate picture of investment performance. Reinvested dividends often account for a massive percentage of total historical stock market gains over long periods."
          }
        },
        {
          "@type": "Question",
          "name": "What is the difference between price return and total return?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Price return only measures the change in a stock's market price from the time you bought it. Total return includes both the price appreciation and any dividends or distributions received during the holding period."
          }
        },
        {
          "@type": "Question",
          "name": "How is the annualized return (CAGR) calculated?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The Compound Annual Growth Rate (CAGR) is calculated by taking the final investment value divided by the initial investment, raised to the power of 1 divided by the number of years held, minus 1. This smooths out returns over the investment period."
          }
        },
        {
          "@type": "Question",
          "name": "Can this stock investment return calculator handle custom dates?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, our stock investment return calculator allows you to select specific historical start and end dates to precisely measure returns and max drawdowns for your specific holding period."
          }
        }
      ]
    }
    </script>
</head>
<body>

<nav class="sticky-nav">
    <a href="/" class="brand">FireMaths</a>
    <div class="links">
        <a href="/#studies">Studies</a>
        <a href="/#tools">Tools</a>
        <a href="/#guides">Guides</a>
    </div>
</nav>

<div class="container">
    <header>
        <h1>Stock Return Calculator</h1>
        <p>Calculate your true total return with dividends reinvested</p>
    </header>

    <div class="dashboard">
        <div class="card">
            <h2>Investment Details</h2>
            <div class="input-group">
                <label for="ticker">Select Ticker (S&P 500 & Popular Stocks)</label>
                <select id="ticker">
                    <option value="SPY">SPY (S&P 500 ETF)</option>
                    <option value="AAPL">AAPL (Apple)</option>
                    <option value="MSFT">MSFT (Microsoft)</option>
                    <option value="GOOGL">GOOGL (Alphabet)</option>
                    <option value="AMZN">AMZN (Amazon)</option>
                    <option value="NVDA">NVDA (Nvidia)</option>
                    <option value="META">META (Meta)</option>
                    <option value="TSLA">TSLA (Tesla)</option>
                    <option value="BRK-B">BRK-B (Berkshire Hathaway)</option>
                </select>
            </div>

            <div class="input-group">
                <label for="buy-date">Buy Month</label>
                <input type="month" id="buy-date" value="2015-01">
            </div>

            <div class="input-group">
                <label for="sell-date">Sell Month</label>
                <input type="month" id="sell-date" value="2024-01">
            </div>

            <div class="input-group">
                <label for="investment">Initial Investment ($)</label>
                <input type="number" id="investment" value="10000" min="1" step="100">
            </div>

            <button class="btn" onclick="calculate()">Calculate Return</button>
        </div>

        <div class="card">
            <h2>Performance Summary</h2>

            <div class="result-item">
                <span class="result-label">Initial Investment</span>
                <span class="result-val" id="res-init">$0.00</span>
            </div>

            <div class="result-item">
                <span class="result-label">Final Value</span>
                <span class="result-val val-pos" id="res-final">$0.00</span>
            </div>

            <div class="result-item">
                <span class="result-label">Price Return</span>
                <span class="result-val" id="res-price-ret">0.00%</span>
            </div>

            <div class="result-item">
                <span class="result-label">Dividend Return</span>
                <span class="result-val val-pos" id="res-div-ret">0.00%</span>
            </div>

            <div class="result-item">
                <span class="result-label">Total Return <button class="copy-btn" onclick="copyVal('res-tot-ret')">Copy</button></span>
                <span class="result-val val-pos" id="res-tot-ret">0.00%</span>
            </div>

            <div class="result-item">
                <span class="result-label">Annualized Return (CAGR) <button class="copy-btn" onclick="copyVal('res-cagr')">Copy</button></span>
                <span class="result-val val-pos" id="res-cagr">0.00%</span>
            </div>

            <div class="result-item">
                <span class="result-label">Max Drawdown</span>
                <span class="result-val val-neg" id="res-drawdown">0.00%</span>
            </div>

            <div class="result-item">
                <span class="result-label">vs S&P 500 (SPY)</span>
                <span class="result-val" id="res-vs-spy">0.00%</span>
            </div>
        </div>
    </div>

    <div class="card">
        <h2>Growth of Investment</h2>
        <div class="chart-container">
            <canvas id="growthChart"></canvas>
        </div>
    </div>

    <div class="faq-section">
        <h2>Frequently Asked Questions</h2>

        <div class="faq-item">
            <h3>How does a stock return calculator work?</h3>
            <p>A stock return calculator computes the total return on an investment by taking the difference between the buy and sell prices, adding any accumulated dividends, and comparing it to the initial amount invested.</p>
        </div>

        <div class="faq-item">
            <h3>Why is a total return calculator with dividends important?</h3>
            <p>Using a total return calculator with dividends gives a more accurate picture of investment performance. Reinvested dividends often account for a massive percentage of total historical stock market gains over long periods.</p>
        </div>

        <div class="faq-item">
            <h3>What is the difference between price return and total return?</h3>
            <p>Price return only measures the change in a stock's market price from the time you bought it. Total return includes both the price appreciation and any dividends or distributions received during the holding period.</p>
        </div>

        <div class="faq-item">
            <h3>How is the annualized return (CAGR) calculated?</h3>
            <p>The Compound Annual Growth Rate (CAGR) is calculated by taking the final investment value divided by the initial investment, raised to the power of 1 divided by the number of years held, minus 1. This smooths out returns over the investment period.</p>
        </div>

        <div class="faq-item">
            <h3>Can this stock investment return calculator handle custom dates?</h3>
            <p>Yes, our stock investment return calculator allows you to select specific historical start and end dates to precisely measure returns and max drawdowns for your specific holding period.</p>
        </div>
    </div>

</div>

<footer>
    © 2026 FireMaths · A GAB Ventures property. Not investment advice. All information for educational purposes only.
</footer>

<script>
    const stockData = DATA_PLACEHOLDER;

    function copyVal(id) {
        const text = document.getElementById(id).innerText;
        navigator.clipboard.writeText(text);
    }

    let chartInstance = null;

    function formatPct(val) {
        if(val === null || isNaN(val)) return "N/A";
        return (val * 100).toFixed(2) + "%";
    }

    function formatCur(val) {
        if(val === null || isNaN(val)) return "N/A";
        return "$" + val.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    }

    function calculate() {
        const ticker = document.getElementById('ticker').value;
        const buyDate = document.getElementById('buy-date').value;
        const sellDate = document.getElementById('sell-date').value;
        const investment = parseFloat(document.getElementById('investment').value);

        if (!stockData[ticker] || !stockData["SPY"]) return;

        // Find indices
        const tData = stockData[ticker];
        const sData = stockData["SPY"];

        let buyIdx = -1, sellIdx = -1;

        for(let i=0; i<tData.dates.length; i++) {
            if (tData.dates[i].startsWith(buyDate) && buyIdx === -1) {
                buyIdx = i;
            }
            if (tData.dates[i].startsWith(sellDate)) {
                sellIdx = i;
            }
        }

        // Fallbacks
        if (buyIdx === -1) buyIdx = 0;
        if (sellIdx === -1) sellIdx = tData.dates.length - 1;
        if (buyIdx > sellIdx) {
            let temp = buyIdx; buyIdx = sellIdx; sellIdx = temp;
        }

        // We simulate purchasing shares and reinvesting dividends monthly.
        // We use adjusted close for total return simulation since it factors in splits and dividends.
        // Wait, yfinance adj close already assumes dividend reinvestment!
        // So total return = AdjClose[sell] / AdjClose[buy] - 1
        // Price return = Close[sell] / Close[buy] - 1
        // Actually, Close in yfinance is split-adjusted but NOT dividend adjusted!
        // So Price return = Close[sell] / Close[buy] - 1

        const buyClose = tData.close[buyIdx];
        const sellClose = tData.close[sellIdx];

        const buyAdj = tData.adj_close[buyIdx];
        const sellAdj = tData.adj_close[sellIdx];

        if (!buyClose || !sellClose || !buyAdj || !sellAdj) {
            alert("Data not available for selected dates.");
            return;
        }

        const priceReturn = (sellClose / buyClose) - 1;
        const totalReturn = (sellAdj / buyAdj) - 1;
        const dividendReturn = totalReturn - priceReturn; // approximation

        const finalValue = investment * (1 + totalReturn);

        // CAGR
        const years = (sellIdx - buyIdx) / 12;
        let cagr = 0;
        if (years > 0) {
            cagr = Math.pow(1 + totalReturn, 1 / years) - 1;
        }

        // Calculate array of values for chart & drawdown
        let peak = 0;
        let maxDrawdown = 0;
        let chartLabels = [];
        let chartData = [];
        let currentShares = investment / tData.adj_close[buyIdx];

        for (let i = buyIdx; i <= sellIdx; i++) {
            let val = currentShares * tData.adj_close[i];
            if (val > peak) peak = val;
            let dd = (val - peak) / peak;
            if (dd < maxDrawdown) maxDrawdown = dd;

            chartLabels.push(tData.dates[i].substring(0, 7));
            chartData.push(val);
        }

        // SPY benchmark
        let spyBuyIdx = -1, spySellIdx = -1;
        for(let i=0; i<sData.dates.length; i++) {
            if (sData.dates[i].startsWith(buyDate) && spyBuyIdx === -1) spyBuyIdx = i;
            if (sData.dates[i].startsWith(sellDate)) spySellIdx = i;
        }
        if (spyBuyIdx === -1) spyBuyIdx = 0;
        if (spySellIdx === -1) spySellIdx = sData.dates.length - 1;
        if (spyBuyIdx > spySellIdx) {
            let temp = spyBuyIdx; spyBuyIdx = spySellIdx; spySellIdx = temp;
        }

        let spyTotalReturn = 0;
        if (sData.adj_close[spyBuyIdx] && sData.adj_close[spySellIdx]) {
            spyTotalReturn = (sData.adj_close[spySellIdx] / sData.adj_close[spyBuyIdx]) - 1;
        }
        const vsSpy = totalReturn - spyTotalReturn;

        // DOM Updates
        document.getElementById('res-init').innerText = formatCur(investment);
        document.getElementById('res-final').innerText = formatCur(finalValue);
        document.getElementById('res-price-ret').innerText = formatPct(priceReturn);
        document.getElementById('res-div-ret').innerText = formatPct(dividendReturn);
        document.getElementById('res-tot-ret').innerText = formatPct(totalReturn);
        document.getElementById('res-cagr').innerText = formatPct(cagr);
        document.getElementById('res-drawdown').innerText = formatPct(maxDrawdown);

        const vsSpyEl = document.getElementById('res-vs-spy');
        vsSpyEl.innerText = formatPct(vsSpy);
        vsSpyEl.className = 'result-val ' + (vsSpy >= 0 ? 'val-pos' : 'val-neg');

        const setCol = (id, val) => {
            document.getElementById(id).className = 'result-val ' + (val >= 0 ? 'val-pos' : 'val-neg');
        };
        setCol('res-price-ret', priceReturn);
        setCol('res-tot-ret', totalReturn);
        setCol('res-cagr', cagr);

        drawChart(chartLabels, chartData);
    }

    function drawChart(labels, data) {
        const canvas = document.getElementById('growthChart');
        const ctx = canvas.getContext('2d');

        // Handle device pixel ratio for crisp text
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

        const w = rect.width;
        const h = rect.height;

        ctx.clearRect(0, 0, w, h);

        if (data.length === 0) return;

        const padding = {top: 20, right: 20, bottom: 30, left: 60};
        const minVal = Math.min(...data) * 0.95;
        const maxVal = Math.max(...data) * 1.05;

        const getX = (i) => padding.left + (i / (data.length - 1 || 1)) * (w - padding.left - padding.right);
        const getY = (val) => h - padding.bottom - ((val - minVal) / (maxVal - minVal)) * (h - padding.top - padding.bottom);

        // Draw grid
        ctx.strokeStyle = '#152040';
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let i = 0; i <= 4; i++) {
            let y = padding.top + (i/4) * (h - padding.top - padding.bottom);
            ctx.moveTo(padding.left, y);
            ctx.lineTo(w - padding.right, y);

            // Y-axis labels
            ctx.fillStyle = '#8a9bb2';
            ctx.font = '10px "JetBrains Mono"';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            let val = maxVal - (i/4)*(maxVal - minVal);
            ctx.fillText("$" + (val >= 1000 ? (val/1000).toFixed(1) + 'k' : val.toFixed(0)), padding.left - 10, y);
        }
        ctx.stroke();

        // X-axis labels
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        const xSteps = Math.min(data.length, 6);
        for(let i=0; i<xSteps; i++) {
            let idx = Math.floor(i * (data.length-1) / (xSteps-1));
            let x = getX(idx);
            ctx.fillText(labels[idx], x, h - padding.bottom + 10);
        }

        // Draw line
        ctx.beginPath();
        ctx.moveTo(getX(0), getY(data[0]));
        for(let i=1; i<data.length; i++) {
            ctx.lineTo(getX(i), getY(data[i]));
        }
        ctx.strokeStyle = '#D4A017';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Gradient fill
        let grad = ctx.createLinearGradient(0, padding.top, 0, h - padding.bottom);
        grad.addColorStop(0, 'rgba(212, 160, 23, 0.3)');
        grad.addColorStop(1, 'rgba(212, 160, 23, 0.0)');

        ctx.lineTo(getX(data.length-1), h - padding.bottom);
        ctx.lineTo(getX(0), h - padding.bottom);
        ctx.fillStyle = grad;
        ctx.fill();
    }

    // Initial calculate on load
    window.onload = () => {
        calculate();
    };

    // Responsive chart
    window.addEventListener('resize', () => {
        calculate();
    });

</script>
</body>
</html>
"""

html_out = html_template.replace("DATA_PLACEHOLDER", json.dumps(data))

with open("public/stock-return-calculator.html", "w") as f:
    f.write(html_out)
