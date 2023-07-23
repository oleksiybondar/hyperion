
/**
 * Converts regular text to HTML by replacing newlines with <br> and spaces with &nbsp;
 * @param {string} text - The regular text to convert
 * @returns {string} The HTML-formatted text
 */
const formatRegularTextToHtml = (text) => {
  return text.replaceAll('\n', '</br>').replaceAll(' ', '&nbsp;');
}

/**
 * Parses NDJSON data and returns an array of parsed JSON objects
 * @param {string} ndjson - The NDJSON data as a single string
 * @returns {Object[]} An array of parsed JSON objects
 */
const ndJsonParse = (ndjson) => {
  return ndjson.trim().split("\n").map((line) => { return JSON.parse(line) })
}

/**
 * Reads and parses NDJSON (Newline Delimited JSON) data from the 'ndjson-data' element in the DOM.
 * @returns {Object[]} An array of parsed JSON objects from the NDJSON data.
 */
const readNdJsonData = () => {
  // Get the 'ndjson-data' element from the DOM
  const jsonDataElt = document.getElementById('ndjson-data');

  // If the element is not found or does not exist, return an empty array
  if (!jsonDataElt) return [];

  // Parse the inner HTML of the 'ndjson-data' element as NDJSON and return an array of parsed JSON objects
  return ndJsonParse(jsonDataElt.innerHTML);
}

/**
 * Capitalizes the first letter of a given string.
 * @param {string} str - The input string to capitalize.
 * @returns {string} The input string with the first letter capitalized.
 */
const capitalise = (str) => {
  // Capitalize the first letter of the input string using the 'charAt' and 'slice' methods
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Splits a camel-cased string into separate words by inserting a space between lowercase and uppercase letters.
 * @param {string} str - The input camel-cased string.
 * @returns {string} The input string with spaces inserted between lowercase and uppercase letters.
 */
const splitCamelCased = (str) => {
  // Use a regular expression to find all occurrences of a lowercase letter followed by an uppercase letter
  // and replace them with the lowercase letter followed by a space and the uppercase letter
  return str.replace(/([a-z])([A-Z])/g, '$1 $2');
}