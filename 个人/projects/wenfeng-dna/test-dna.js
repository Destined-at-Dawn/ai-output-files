const parseDNAString = require('./dist/index.js').parseDNAString || (() => null);

// 简单的本地测试
const dnaStr = "PH911EP111ID5555555RHNLCGVT1SY09001E000100000DN98808SK8RD555151";
console.log("Testing DNA:", dnaStr);
console.log("PH match:", dnaStr.match(/PH(\d{2})([1-6])([1-5])/));
console.log("EP match:", dnaStr.match(/EP([1-5])([1-5])([1-4])/));
console.log("ID match:", dnaStr.match(/ID(\d{7})/));
console.log("RH match:", dnaStr.match(/RH([A-Z]{3})([A-Z]{3})([1359])/));
console.log("SY match:", dnaStr.match(/SY(\d{2})(\d{2})([135])([A-Z]{2})(\d{3})(\d{3})(\d{3})/));
console.log("DN match:", dnaStr.match(/DN([1-9])([1-9])([1-9])([1-9])([A-Z0-9]{2})([1-9])/));
console.log("RD match:", dnaStr.match(/RD([1-9])([1-9])([1-9])([1-9])([1-9])([1-9])/));
