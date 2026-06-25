const { WenfengEncoder, serializeDNA, parseDNAString, getDefaultVocabularyManager } = require('./dist/index');

const encoder = new WenfengEncoder('我试过这个方法，效果真的太惊艳了！油皮姐妹闭眼入，绝对不踩雷。', getDefaultVocabularyManager().getBank('SK'));
const result = encoder.encode();

console.log('=== DNA Object ===');
console.log(JSON.stringify(result.dna, null, 2));

console.log('\n=== Serialized DNA ===');
const serialized = serializeDNA(result.dna);
console.log(serialized);

console.log('\n=== Parse Test ===');
const parsed = parseDNAString(serialized);
console.log(parsed ? 'PASS' : 'FAIL');
if (parsed) {
  console.log('Parsed matches original:', JSON.stringify(parsed) === JSON.stringify(result.dna) ? 'YES' : 'NO');
}
