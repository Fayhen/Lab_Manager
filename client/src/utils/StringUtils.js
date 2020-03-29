export function ParseName(first, middle, last) {
  let personName = '';

  if (middle) {
    personName = `${first} ${middle} ${last}`;
  } else {
    personName = `${first} ${last}`;
  }

  return personName;
}

export function CapitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
