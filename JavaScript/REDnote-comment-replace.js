// 支持 argument: pattern=xxx&replace=yyy
(function () {
  let body = $response.body || '';
  const args = Object.fromEntries(
    (($argument || '').split('&').filter(Boolean).map(kv => kv.split('='))) // [['pattern','red_id'],['replace','fmz200']]
    .map(([k, v = '']) => [decodeURIComponent(k), decodeURIComponent(v)])
  );
  const pattern = args.pattern ? new RegExp(args.pattern, 'g') : /red_id/g;
  const replacement = args.replace || 'fmz200';
  body = body.replace(pattern, replacement);
  $done({ body });
})();
