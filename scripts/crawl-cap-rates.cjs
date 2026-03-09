const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');

// Map of state abbreviations to full names for matching with Census data
const stateMap = {
  "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
  "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
  "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
  "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
  "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
  "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
  "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
  "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
  "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
  "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
  "DC": "District of Columbia"
};

async function scrapeCities() {
  try {
    const res = await axios.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population', {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
    });
    const $ = cheerio.load(res.data);
    const cities = [];
    const fullToAbbrev = Object.fromEntries(Object.entries(stateMap).map(([k, v]) => [v, k]));

    $('table.wikitable.sortable').first().find('tbody tr').each((i, el) => {
      const city = $(el).find('td').eq(0).text().trim().replace(/\[.*?\]/, '').replace(/^\d+$/, '').trim();
      let state = $(el).find('td').eq(1).text().trim().replace(/\[.*?\]/, '').trim();

      if (state === "Washington, D.C." || state === "District of Columbia") {
          state = "DC";
      } else if (fullToAbbrev[state]) {
          state = fullToAbbrev[state]; // Convert full name to abbreviation (e.g. New York -> NY)
      }

      if (city && state && cities.length < 50) {
        cities.push({ city, state });
      }
    });
    return cities;
  } catch (e) {
    console.error("Failed to fetch cities from Wikipedia:", e.message);
    return null;
  }
}

async function fetchCensusData() {
  try {
    // DP04_0089E is Median Value (Dollars)
    // DP04_0134E is Median Gross Rent (Dollars)
    const res = await axios.get('https://api.census.gov/data/2022/acs/acs1/profile?get=NAME,DP04_0089E,DP04_0134E&for=place:*', {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
    });

    const data = res.data;
    const cityDataMap = {};

    for (let i = 1; i < data.length; i++) {
      const [name, medianValueStr, medianRentStr] = data[i];
      // Name looks like "New York city, New York" or "Gilbert town, Arizona"
      const cleanedName = name.replace(/ (city|town|CDP|municipality|village),/, ',');

      const medianPrice = medianValueStr && medianValueStr !== "-666666666" ? parseInt(medianValueStr) : null;
      const avgRentMonthly = medianRentStr && medianRentStr !== "-666666666" ? parseInt(medianRentStr) : null;

      cityDataMap[cleanedName] = { medianPrice, avgRentMonthly };
    }

    return cityDataMap;
  } catch (e) {
    console.error("Failed to fetch census data:", e.message);
    return null;
  }
}

async function run() {
  const cities = await scrapeCities();
  if (!cities) {
    console.error("Failed to get list of cities.");
    return;
  }

  const censusDataMap = await fetchCensusData();
  const results = [];

  for (const cityObj of cities) {
    const { city, state } = cityObj;
    console.log(`Processing data for ${city}, ${state}...`);

    let medianPrice = null;
    let avgRentMonthly = null;
    let capRate = null;
    let priceToRent = null;
    let popGrowth = null;
    let jobGrowth = null;

    const stateFullName = stateMap[state];

    // Some cities in Wikipedia might be written as "Nashville-Davidson" but in Census as "Nashville-Davidson metropolitan government (balance)"
    // We will do a generic lookup
    let lookupKey = `${city}, ${stateFullName}`;

    if (censusDataMap && censusDataMap[lookupKey]) {
      medianPrice = censusDataMap[lookupKey].medianPrice;
      avgRentMonthly = censusDataMap[lookupKey].avgRentMonthly;
    } else if (censusDataMap) {
      // Try finding a partial match in the same state
      const possibleKeys = Object.keys(censusDataMap).filter(k => k.includes(city) && k.includes(stateFullName));
      if (possibleKeys.length > 0) {
        medianPrice = censusDataMap[possibleKeys[0]].medianPrice;
        avgRentMonthly = censusDataMap[possibleKeys[0]].avgRentMonthly;
      }
    }

    if (avgRentMonthly && medianPrice) {
      const annualRent = avgRentMonthly * 12;
      const expenses = annualRent * 0.45; // Est. 45% expenses (property tax, maintenance, vacancy, insurance, management)
      const netOperatingIncome = annualRent - expenses;
      capRate = parseFloat(((netOperatingIncome / medianPrice) * 100).toFixed(2));
      priceToRent = parseFloat((medianPrice / annualRent).toFixed(2));
    }

    results.push({
      city,
      state,
      medianPrice,
      avgRentMonthly,
      capRate,
      priceToRent,
      popGrowth,
      jobGrowth
    });

    // Simulate scraping delay
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  // Write output
  if (!fs.existsSync('data')) {
    fs.mkdirSync('data');
  }
  fs.writeFileSync('data/cap-rates.json', JSON.stringify(results, null, 2));
  console.log(`Saved ${results.length} cities to data/cap-rates.json`);
}

run();