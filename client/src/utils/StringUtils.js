/**
 * Parses separated strings representing a person's first, last and middle
 * names. All arguments must be strings, including empty strings where one
 * of the names is unavailable.
 *
 * Returns a single string with the person's full name, first to last.
 *
 * @param {string} first - Person's first name(s).
 * @param {string} middle - Person's middle name(s) or empty string.
 * @param {string} last - Person's last name(s).
*/
export function ParseName(first, middle, last) {
  let personName = '';

  if (middle) {
    personName = `${first} ${middle} ${last}`;
  } else {
    personName = `${first} ${last}`;
  }

  return personName;
}

/**
 * Capitalizes the first letter of any given string.
 *
 * @param {string} string - Any string.
*/
export function CapitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * Takes a unix timestamp and uses it to create a new Date instance. Next,
 * casts the Date instance to a string on the format "D/M/YYYY".
 *
 * Returns a date string on the format "D/M/YYYY".
 *
 *@param {string|number} unixtime - Unix timestamp to be parsed.
*/
export function ParseDate(unixtime) {
  const intDate = typeof unixtime === 'number' ? unixtime : parseInt(unixtime, 10);
  const casted = new Date(intDate);
  const parsedDate = `${casted.getDate()}/${casted.getMonth() + 1}/${casted.getFullYear()}`;

  return parsedDate;
}

/**
 * Take a date string on the "D/M/YYYY" format and uses it to create a new
 * Date instance. Generates a unixtime number using the built-in .getTime()
 * function on the new Date instance.
 *
 * Returns the generated unixtime as a string.
 *
 * @param {string} date - String containing date. Must on the"D/M/YYYY" format.
*/
export function DateToUnix(date) {
  // console.log(typeof date);
  // console.log(date);
  const dmy = date.split('/');
  // console.log(dmy);
  const parsed = new Date(dmy[2], dmy[1] - 1, dmy[0]);
  // console.log(parsed);
  const unixtime = parsed.getTime();
  // console.log(unixtime);
  // console.log(ParseDate(unixtime));

  return unixtime.toString();
}
