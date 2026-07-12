export const createElement = (tagName, options = {}) => {
  const element = document.createElement(tagName);
  if (options.className) element.className = options.className;
  if (options.text !== undefined) element.textContent = options.text;
  Object.entries(options.attributes || {}).forEach(([name, value]) => {
    if (value !== undefined && value !== null) element.setAttribute(name, String(value));
  });
  return element;
};

export const createLink = (className, href, text) => createElement("a", {
  className,
  text,
  attributes: { href }
});

export const createSvgElement = (tagName, attributes = {}) => {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tagName);
  Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, String(value)));
  return element;
};
