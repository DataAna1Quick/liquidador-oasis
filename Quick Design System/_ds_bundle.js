/* @ds-bundle: {"format":3,"namespace":"QuickDesignSystem_adff9f","components":[{"name":"Header","sourcePath":"components/brand/Header.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Expander","sourcePath":"components/core/Expander.jsx"},{"name":"MetricTile","sourcePath":"components/core/MetricTile.jsx"},{"name":"DataTable","sourcePath":"components/data/DataTable.jsx"},{"name":"AlertPanel","sourcePath":"components/feedback/AlertPanel.jsx"},{"name":"FileDropzone","sourcePath":"components/forms/FileDropzone.jsx"}],"sourceHashes":{"components/brand/Header.jsx":"6f4b4d7855d9","components/core/Badge.jsx":"b3ed8ad56ded","components/core/Button.jsx":"89b56dc6bf94","components/core/Card.jsx":"5940c12b2720","components/core/Expander.jsx":"3737e1edd621","components/core/MetricTile.jsx":"5310b06120ac","components/data/DataTable.jsx":"0373b358eb5f","components/feedback/AlertPanel.jsx":"23995a1df8ee","components/forms/FileDropzone.jsx":"27c685dfdf86","ui_kits/liquidacion/PayrollScreen.jsx":"0e51e5150c5b"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.QuickDesignSystem_adff9f = window.QuickDesignSystem_adff9f || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/brand/Header.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Header — the fixed black brand bar.
 * Logo (Q with yellow bolt) + title + version subtitle, optional right slot.
 * The logo sits on black with NO shadow or effect (brand law). Pass the
 * inverse (white-ring) logo so it reads on the dark bar.
 */
function Header({
  logoSrc = 'assets/quick-logo-inverse.png',
  title = 'Liquidación de Nómina',
  version = 'v2.4',
  subtitle = null,
  right = null,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("header", _extends({
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-4)',
      padding: '0 var(--space-6)',
      minHeight: 'var(--header-h)',
      background: 'var(--quick-black)',
      color: 'var(--quick-white)',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("img", {
    src: logoSrc,
    alt: "Quick",
    style: {
      height: 55,
      width: 'auto',
      display: 'block'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      gap: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-h2)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--quick-white)',
      lineHeight: 1.15
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--ink-300)',
      fontWeight: 'var(--fw-light)'
    }
  }, subtitle ? subtitle : /*#__PURE__*/React.createElement(React.Fragment, null, "Herramienta interna \xB7 ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--quick-yellow)',
      fontWeight: 'var(--fw-regular)'
    }
  }, version)))), right && /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto',
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-3)'
    }
  }, right));
}
Object.assign(__ds_scope, { Header });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Header.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — compact status / conciliation marker.
 * Status is conveyed WITHOUT hue (brand law: no green/red).
 *  - ok:      solid black chip, white text + check glyph
 *  - review:  yellow-washed chip, black text, yellow rule + alert glyph, bold
 *  - neutral: light-grey chip, muted text
 *  - accent:  solid yellow chip, black text
 */
function Badge({
  status = 'neutral',
  children,
  icon = null,
  style = {},
  ...rest
}) {
  const variants = {
    ok: {
      background: 'var(--status-ok-bg)',
      color: 'var(--status-ok-fg)',
      border: '1px solid var(--status-ok-bg)',
      fontWeight: 'var(--fw-bold)'
    },
    review: {
      background: 'var(--status-review-bg)',
      color: 'var(--status-review-fg)',
      border: '1px solid var(--status-review-line)',
      fontWeight: 'var(--fw-bold)'
    },
    neutral: {
      background: 'var(--quick-grey)',
      color: 'var(--text-muted)',
      border: '1px solid var(--line-200)',
      fontWeight: 'var(--fw-bold)'
    },
    accent: {
      background: 'var(--quick-yellow)',
      color: 'var(--quick-black)',
      border: '1px solid var(--quick-yellow)',
      fontWeight: 'var(--fw-bold)'
    }
  };
  const v = variants[status] || variants.neutral;
  const defaultGlyph = status === 'ok' ? '✓' : status === 'review' ? '!' : null;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      padding: '4px 10px',
      borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-label)',
      lineHeight: 1,
      letterSpacing: '0.02em',
      whiteSpace: 'nowrap',
      ...v,
      ...style
    }
  }, rest), icon ?? (defaultGlyph && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 14,
      height: 14,
      borderRadius: '50%',
      fontSize: 10,
      fontWeight: 700,
      background: status === 'ok' ? 'var(--quick-yellow)' : 'var(--quick-black)',
      color: status === 'ok' ? 'var(--quick-black)' : 'var(--quick-yellow)'
    }
  }, defaultGlyph)), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Quick Button — the primary action surface.
 * Variants stay strictly inside the brand palette:
 *  - primary:   yellow fill, black text  (the main CTA, e.g. "Descargar Excel")
 *  - dark:      black fill, white text
 *  - secondary: white fill, black border
 *  - ghost:     transparent, black text
 */
function Button({
  variant = 'primary',
  size = 'md',
  iconLeft = null,
  iconRight = null,
  disabled = false,
  block = false,
  children,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      padding: '6px 12px',
      fontSize: 'var(--fs-label)',
      gap: '6px',
      height: 32
    },
    md: {
      padding: '10px 18px',
      fontSize: 'var(--fs-body)',
      gap: '8px',
      height: 40
    },
    lg: {
      padding: '14px 24px',
      fontSize: 'var(--fs-h3)',
      gap: '10px',
      height: 52
    }
  };
  const variants = {
    primary: {
      background: 'var(--quick-yellow)',
      color: 'var(--quick-black)',
      border: '1px solid var(--quick-yellow)'
    },
    dark: {
      background: 'var(--quick-black)',
      color: 'var(--quick-white)',
      border: '1px solid var(--quick-black)'
    },
    secondary: {
      background: 'var(--quick-white)',
      color: 'var(--quick-black)',
      border: '1px solid var(--quick-black)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--quick-black)',
      border: '1px solid transparent'
    }
  };
  const s = sizes[size] || sizes.md;
  const v = variants[variant] || variants.primary;
  return /*#__PURE__*/React.createElement("button", _extends({
    disabled: disabled,
    style: {
      display: block ? 'flex' : 'inline-flex',
      width: block ? '100%' : 'auto',
      alignItems: 'center',
      justifyContent: 'center',
      gap: s.gap,
      padding: s.padding,
      minHeight: s.height,
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--fw-bold)',
      fontSize: s.fontSize,
      lineHeight: 1,
      letterSpacing: '0.01em',
      borderRadius: 'var(--radius-md)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.4 : 1,
      transition: 'transform var(--dur-fast) var(--ease-standard), filter var(--dur-fast) var(--ease-standard)',
      ...v,
      ...style
    },
    onMouseDown: e => {
      if (!disabled) e.currentTarget.style.transform = 'translateY(1px)';
    },
    onMouseUp: e => {
      e.currentTarget.style.transform = 'translateY(0)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.filter = 'none';
    },
    onMouseEnter: e => {
      if (!disabled) e.currentTarget.style.filter = 'brightness(0.94)';
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — the base surface container.
 * Flat white panel, hairline border, optional safety-tape top accent.
 * No soft elevation by default — the brand reads as tooling.
 */
function Card({
  tape = false,
  padded = true,
  title = null,
  action = null,
  children,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("section", _extends({
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      ...style
    }
  }, rest), tape && /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      height: 'var(--tape-height)',
      background: 'var(--tape)',
      backgroundSize: '33.94px 33.94px'
    }
  }), (title || action) && /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 'var(--space-3)',
      padding: '14px 18px',
      borderBottom: '1px solid var(--border-default)'
    }
  }, typeof title === 'string' ? /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: 'var(--fs-h3)'
    }
  }, title) : title, action), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: padded ? 'var(--space-5)' : 0
    }
  }, children));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Expander.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Expander — a collapsible disclosure section (used for "Historial" and any
 * secondary content). Black header bar with a rotating chevron; body reveals
 * below. Controlled or uncontrolled.
 */
function Expander({
  title,
  subtitle = null,
  defaultOpen = false,
  open: controlledOpen,
  onToggle,
  children,
  style = {},
  ...rest
}) {
  const [internal, setInternal] = React.useState(defaultOpen);
  const open = controlledOpen ?? internal;
  const toggle = () => {
    onToggle ? onToggle(!open) : setInternal(!open);
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      background: 'var(--surface-card)',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("button", {
    onClick: toggle,
    "aria-expanded": open,
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      width: '100%',
      gap: 'var(--space-3)',
      padding: '14px 18px',
      background: 'var(--surface-card)',
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-sans)',
      textAlign: 'left'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 2
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-h3)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-strong)'
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, subtitle)), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 28,
      height: 28,
      flex: '0 0 auto',
      borderRadius: 'var(--radius-sm)',
      background: 'var(--quick-black)',
      color: 'var(--quick-yellow)',
      transform: open ? 'rotate(180deg)' : 'rotate(0deg)',
      transition: 'transform var(--dur-base) var(--ease-standard)',
      fontSize: 12,
      fontWeight: 700
    }
  }, "\u25BE")), open && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-5)',
      borderTop: '1px solid var(--border-default)'
    }
  }, children));
}
Object.assign(__ds_scope, { Expander });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Expander.jsx", error: String((e && e.message) || e) }); }

// components/core/MetricTile.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * MetricTile — a single KPI cell used in the metrics row
 * (periodo, filas, empleados, ajustes). Large light numeral, uppercase label,
 * optional unit and yellow accent tick.
 */
function MetricTile({
  label,
  value,
  unit = null,
  hint = null,
  accent = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      padding: 'var(--space-5)',
      minWidth: 0,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      top: 0,
      left: 'var(--space-5)',
      width: 28,
      height: 4,
      background: accent ? 'var(--quick-yellow)' : 'var(--quick-black)',
      borderRadius: '0 0 2px 2px'
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "q-overline",
    style: {
      fontSize: 'var(--fs-micro)',
      fontWeight: 'var(--fw-bold)',
      letterSpacing: 'var(--ls-overline)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)',
      marginBottom: 'var(--space-3)'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-display)',
      fontWeight: 'var(--fw-light)',
      letterSpacing: 'var(--ls-tight)',
      color: 'var(--text-strong)',
      lineHeight: 1,
      fontVariantNumeric: 'tabular-nums'
    }
  }, value), unit && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-muted)'
    }
  }, unit)), hint && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6,
      fontSize: 'var(--fs-label)',
      color: 'var(--text-subtle)'
    }
  }, hint));
}
Object.assign(__ds_scope, { MetricTile });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/MetricTile.jsx", error: String((e && e.message) || e) }); }

// components/data/DataTable.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * DataTable — totals/breakdown table (e.g. totales por concepto).
 * Dense, tabular figures, sticky-styled black header. Right-aligns numeric
 * columns automatically when align="right" is set on the column.
 * columns: [{ key, label, align?, render?, width? }]
 * Optional totals row via the `totals` prop (same shape as a row).
 */
function DataTable({
  columns = [],
  rows = [],
  totals = null,
  style = {},
  ...rest
}) {
  const cell = (col, val, isHead, isTotal) => ({
    padding: '11px 16px',
    textAlign: col.align || 'left',
    fontSize: 'var(--fs-body)',
    fontVariantNumeric: col.align === 'right' ? 'tabular-nums' : 'normal',
    fontWeight: isHead ? 'var(--fw-bold)' : isTotal ? 'var(--fw-bold)' : 'var(--fw-regular)',
    color: isHead ? 'var(--quick-white)' : 'var(--text-body)',
    whiteSpace: 'nowrap',
    width: col.width || 'auto'
  });
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      overflowX: 'auto',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      borderCollapse: 'collapse',
      fontFamily: 'var(--font-sans)'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: 'var(--quick-black)'
    }
  }, columns.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.key,
    style: {
      ...cell(c, null, true),
      letterSpacing: '0.04em',
      fontSize: 'var(--fs-label)'
    }
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, i) => /*#__PURE__*/React.createElement("tr", {
    key: i,
    style: {
      background: i % 2 ? 'var(--quick-grey)' : 'var(--quick-white)'
    }
  }, columns.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.key,
    style: {
      ...cell(c, r[c.key], false, false),
      borderBottom: '1px solid var(--line-100)'
    }
  }, c.render ? c.render(r[c.key], r) : r[c.key]))))), totals && /*#__PURE__*/React.createElement("tfoot", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: 'var(--surface-wash)',
      borderTop: '2px solid var(--quick-black)'
    }
  }, columns.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.key,
    style: {
      ...cell(c, totals[c.key], false, true)
    }
  }, c.render ? c.render(totals[c.key], totals) : totals[c.key]))))));
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/DataTable.jsx", error: String((e && e.message) || e) }); }

// components/feedback/AlertPanel.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * AlertPanel — collapsible panel listing reconciliation alerts.
 * Header shows a count badge; body lists items. Severity is encoded without
 * hue: "review" items get a yellow tick + bold label, "info" stays neutral.
 */
function AlertPanel({
  title = 'Alertas',
  items = [],
  defaultOpen = true,
  style = {},
  ...rest
}) {
  const [open, setOpen] = React.useState(defaultOpen);
  const count = items.length;
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      background: 'var(--surface-card)',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("button", {
    onClick: () => setOpen(!open),
    "aria-expanded": open,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-3)',
      width: '100%',
      padding: '14px 18px',
      cursor: 'pointer',
      textAlign: 'left',
      background: 'var(--surface-card)',
      border: 'none',
      fontFamily: 'var(--font-sans)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 26,
      height: 26,
      borderRadius: 'var(--radius-sm)',
      flex: '0 0 auto',
      background: count ? 'var(--quick-yellow)' : 'var(--quick-grey)',
      color: 'var(--quick-black)',
      fontWeight: 700,
      fontSize: 14
    }
  }, count ? '!' : '✓'), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-h3)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-strong)'
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 4,
      padding: '2px 8px',
      borderRadius: 'var(--radius-pill)',
      background: 'var(--quick-black)',
      color: 'var(--quick-white)',
      fontSize: 'var(--fs-micro)',
      fontWeight: 700,
      fontVariantNumeric: 'tabular-nums'
    }
  }, count), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      marginLeft: 'auto',
      color: 'var(--text-muted)',
      fontSize: 12,
      fontWeight: 700,
      transform: open ? 'rotate(180deg)' : 'rotate(0)',
      transition: 'transform var(--dur-base) var(--ease-standard)'
    }
  }, "\u25BE")), open && /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: 'none',
      margin: 0,
      padding: 0,
      borderTop: '1px solid var(--border-default)'
    }
  }, items.length === 0 && /*#__PURE__*/React.createElement("li", {
    style: {
      padding: '14px 18px',
      color: 'var(--text-muted)',
      fontSize: 'var(--fs-label)'
    }
  }, "Sin alertas. Todo concilia."), items.map((it, i) => {
    const obj = typeof it === 'string' ? {
      text: it,
      severity: 'info'
    } : it;
    const review = obj.severity === 'review';
    return /*#__PURE__*/React.createElement("li", {
      key: i,
      style: {
        display: 'flex',
        alignItems: 'flex-start',
        gap: 'var(--space-3)',
        padding: '12px 18px',
        borderTop: i === 0 ? 'none' : '1px solid var(--line-100)',
        background: review ? 'var(--surface-wash)' : 'transparent'
      }
    }, /*#__PURE__*/React.createElement("span", {
      "aria-hidden": "true",
      style: {
        marginTop: 2,
        width: 8,
        height: 8,
        flex: '0 0 auto',
        borderRadius: 2,
        background: review ? 'var(--quick-yellow)' : 'var(--ink-300)',
        outline: review ? '1px solid var(--quick-black)' : 'none'
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        minWidth: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 'var(--fs-body)',
        color: 'var(--text-body)',
        fontWeight: review ? 'var(--fw-bold)' : 'var(--fw-regular)'
      }
    }, obj.text), obj.detail && /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 'var(--fs-label)',
        color: 'var(--text-muted)',
        marginTop: 2
      }
    }, obj.detail)));
  })));
}
Object.assign(__ds_scope, { AlertPanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/AlertPanel.jsx", error: String((e && e.message) || e) }); }

// components/forms/FileDropzone.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * FileDropzone — the primary action surface of the liquidación tool.
 * Large drag & drop target for the nómina source file (.xlsx / .csv).
 * Drag-over state lights the border yellow and washes the surface.
 * Purely cosmetic file handling — wire onFile to your own logic.
 */
function FileDropzone({
  accept = '.xlsx,.csv',
  hint = 'Arrastra el archivo de novedades o haz clic para seleccionar',
  fileName = null,
  onFile,
  style = {},
  ...rest
}) {
  const [drag, setDrag] = React.useState(false);
  const inputRef = React.useRef(null);
  const pick = f => {
    if (f && onFile) onFile(f);
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    onDragOver: e => {
      e.preventDefault();
      setDrag(true);
    },
    onDragLeave: () => setDrag(false),
    onDrop: e => {
      e.preventDefault();
      setDrag(false);
      pick(e.dataTransfer.files?.[0]);
    },
    onClick: () => inputRef.current?.click(),
    role: "button",
    tabIndex: 0,
    style: {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 'var(--space-3)',
      textAlign: 'center',
      padding: 'var(--space-8) var(--space-5)',
      background: drag ? 'var(--surface-wash)' : 'var(--surface-card)',
      border: `2px dashed ${drag ? 'var(--quick-yellow)' : 'var(--ink-300)'}`,
      borderRadius: 'var(--radius-lg)',
      cursor: 'pointer',
      transition: 'background var(--dur-base) var(--ease-standard), border-color var(--dur-base) var(--ease-standard)',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("input", {
    ref: inputRef,
    type: "file",
    accept: accept,
    hidden: true,
    onChange: e => pick(e.target.files?.[0])
  }), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 56,
      height: 56,
      borderRadius: 'var(--radius-md)',
      background: 'var(--quick-black)',
      color: 'var(--quick-yellow)',
      fontSize: 26,
      fontWeight: 700,
      lineHeight: 1
    }
  }, "\u2191"), fileName ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--fs-h3)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-strong)'
    }
  }, fileName), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, "Clic para reemplazar")) : /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--fs-h3)',
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-strong)'
    }
  }, hint), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)',
      marginTop: 4
    }
  }, "Formatos aceptados: ", accept.replaceAll(',', ', '))));
}
Object.assign(__ds_scope, { FileDropzone });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/FileDropzone.jsx", error: String((e && e.message) || e) }); }

// ui_kits/liquidacion/PayrollScreen.jsx
try { (() => {
/* PayrollScreen — full "Liquidación de Nómina" page for Quick.
   Composes the DS primitives with fake settlement data (horas extra,
   recargos nocturnos). Interactive: empty dropzone → processed dashboard. */

const {
  Header,
  FileDropzone,
  MetricTile,
  Card,
  Badge,
  DataTable,
  AlertPanel,
  Expander,
  Button
} = window.QuickDesignSystem_adff9f;
const CONCEPTOS = [{
  concepto: 'Hora extra diurna (HED)',
  horas: '412,0',
  factor: '1,25',
  equ: '$ 9.870.300'
}, {
  concepto: 'Hora extra nocturna (HEN)',
  horas: '188,5',
  factor: '1,75',
  equ: '$ 6.318.420'
}, {
  concepto: 'Recargo nocturno (RN)',
  horas: '534,0',
  factor: '0,35',
  equ: '$ 3.742.110'
}, {
  concepto: 'Recargo dominical (RD)',
  horas: '149,5',
  factor: '1,75',
  equ: '$ 5.014.880'
}, {
  concepto: 'Hora extra dominical (HEDF)',
  horas: '64,0',
  factor: '2,00',
  equ: '$ 2.156.040'
}, {
  concepto: 'Auxilio de transporte',
  horas: '—',
  factor: '—',
  equ: '$ 1.624.000'
}];
const TOTALS = {
  concepto: 'Total liquidado',
  horas: '1.348,0',
  factor: '—',
  equ: '$ 28.725.750'
};
const ALERTS = [{
  text: 'Recargo nocturno excede el tope legal en 4 registros',
  detail: 'Centro de costo: Bodega Norte · turno 22:00–06:00',
  severity: 'review'
}, {
  text: 'Horas extra dominicales sin autorización previa en 2 empleados',
  detail: 'Conductores · ruta Bogotá–Medellín',
  severity: 'review'
}, {
  text: 'Hora extra diurna supera 2h/día en 1 registro',
  detail: 'Operario · CC Despacho',
  severity: 'review'
}, {
  text: '2 empleados sin centro de costo asignado',
  detail: 'Se liquidan en CC genérico',
  severity: 'info'
}];
const HISTORY = [{
  periodo: 'Mayo 2026 · Q1',
  empleados: '246',
  total: '$ 27.180.400',
  estado: 'ok'
}, {
  periodo: 'Abril 2026 · Q2',
  empleados: '244',
  total: '$ 26.905.110',
  estado: 'ok'
}, {
  periodo: 'Abril 2026 · Q1',
  empleados: '241',
  total: '$ 28.044.730',
  estado: 'review'
}, {
  periodo: 'Marzo 2026 · Q2',
  empleados: '240',
  total: '$ 25.610.980',
  estado: 'ok'
}];
function SectionLabel({
  children,
  step
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      margin: '0 0 12px'
    }
  }, step && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 22,
      height: 22,
      borderRadius: 'var(--radius-sm)',
      background: 'var(--quick-black)',
      color: 'var(--quick-yellow)',
      fontSize: 12,
      fontWeight: 700,
      flex: '0 0 auto'
    }
  }, step), /*#__PURE__*/React.createElement("span", {
    className: "q-overline",
    style: {
      fontSize: 'var(--fs-label)',
      letterSpacing: '0.12em'
    }
  }, children));
}
function PayrollScreen() {
  const [fileName, setFileName] = React.useState('novedades_mayo_2026_q2.xlsx');
  const processed = !!fileName;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: '100vh',
      background: 'var(--surface-page)',
      display: 'flex',
      flexDirection: 'column'
    }
  }, /*#__PURE__*/React.createElement(Header, {
    logoSrc: "../../assets/quick-logo-inverse.png",
    title: "Liquidaci\xF3n de N\xF3mina",
    version: "v2.4",
    right: /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 14
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 'var(--fs-label)',
        color: 'var(--ink-300)'
      }
    }, "Direcci\xF3n de Operaciones"), /*#__PURE__*/React.createElement("span", {
      style: {
        width: 34,
        height: 34,
        borderRadius: '50%',
        background: 'var(--quick-yellow)',
        color: 'var(--quick-black)',
        fontWeight: 700,
        fontSize: 14,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    }, "DO"))
  }), /*#__PURE__*/React.createElement("div", {
    className: "q-tape"
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      width: '100%',
      maxWidth: 'var(--page-max)',
      margin: '0 auto',
      padding: 'var(--space-6) var(--space-5) var(--space-7)',
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("section", {
    style: {
      marginBottom: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement(SectionLabel, {
    step: "1"
  }, "Cargar novedades del periodo"), /*#__PURE__*/React.createElement(FileDropzone, {
    fileName: fileName,
    onFile: f => setFileName(f.name)
  }), processed && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 12,
      marginTop: 12,
      padding: '12px 16px',
      background: 'var(--quick-white)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-md)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, "Procesado el 31 may 2026, 09:14 \xB7 1.482 filas le\xEDdas \xB7 248 empleados"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    onClick: () => setFileName('')
  }, "Cambiar archivo"))), !processed && /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--fs-label)',
      textAlign: 'center',
      marginTop: 40
    }
  }, "Carga el archivo de novedades para ver el resumen de liquidaci\xF3n."), processed && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    style: {
      marginBottom: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement(SectionLabel, {
    step: "2"
  }, "Resumen del periodo"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(MetricTile, {
    label: "Periodo",
    value: "Mayo",
    hint: "2026 \xB7 quincena 2"
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "Filas",
    value: "1.482",
    unit: "reg",
    hint: "0 descartadas"
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "Empleados",
    value: "248",
    hint: "2 inactivos"
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "Ajustes",
    value: "3",
    accent: true,
    hint: "requieren revisi\xF3n"
  }))), /*#__PURE__*/React.createElement("section", {
    style: {
      marginBottom: 'var(--space-6)',
      display: 'grid',
      gridTemplateColumns: '1.6fr 1fr',
      gap: 'var(--space-5)',
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    tape: true,
    padded: false,
    title: "Totales por concepto",
    action: /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 'var(--fs-label)',
        color: 'var(--text-muted)'
      }
    }, "Mayo 2026 \xB7 Q2")
  }, /*#__PURE__*/React.createElement(DataTable, {
    columns: [{
      key: 'concepto',
      label: 'CONCEPTO'
    }, {
      key: 'horas',
      label: 'HORAS',
      align: 'right',
      width: '110px'
    }, {
      key: 'factor',
      label: 'FACTOR',
      align: 'right',
      width: '90px'
    }, {
      key: 'equ',
      label: 'EQUIVALENTE',
      align: 'right',
      width: '150px'
    }],
    rows: CONCEPTOS,
    totals: TOTALS
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Conciliaci\xF3n"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, "Base contra n\xF3mina"), /*#__PURE__*/React.createElement(Badge, {
    status: "ok"
  }, "Cuadra")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, "Topes legales"), /*#__PURE__*/React.createElement(Badge, {
    status: "review"
  }, "Revisar \xB7 3")), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 1,
      background: 'var(--line-200)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, "Diferencia neta"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-h2)',
      fontWeight: 'var(--fw-light)',
      fontVariantNumeric: 'tabular-nums'
    }
  }, "$ 0")))), /*#__PURE__*/React.createElement(AlertPanel, {
    title: "Alertas",
    items: ALERTS,
    defaultOpen: true
  }))), /*#__PURE__*/React.createElement("section", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 16,
      padding: 'var(--space-5)',
      background: 'var(--quick-black)',
      borderRadius: 'var(--radius-lg)',
      marginBottom: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--quick-white)',
      fontSize: 'var(--fs-h3)',
      fontWeight: 'var(--fw-bold)'
    }
  }, "Liquidaci\xF3n lista para exportar"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--ink-300)',
      fontSize: 'var(--fs-label)',
      marginTop: 2
    }
  }, "Incluye detalle por empleado, concepto y centro de costo.")), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    iconLeft: /*#__PURE__*/React.createElement("span", {
      "aria-hidden": "true",
      style: {
        fontSize: 16
      }
    }, "\u2193")
  }, "Descargar Excel")), /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement(Expander, {
    title: "Historial de liquidaciones",
    subtitle: "\xDAltimos 4 periodos procesados",
    defaultOpen: false
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column'
    }
  }, HISTORY.map((h, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: 'grid',
      gridTemplateColumns: '1.4fr 1fr 1fr auto',
      alignItems: 'center',
      gap: 12,
      padding: '12px 4px',
      borderTop: i === 0 ? 'none' : '1px solid var(--line-100)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 'var(--fw-bold)',
      color: 'var(--text-strong)',
      fontSize: 'var(--fs-body)'
    }
  }, h.periodo), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--fs-label)'
    }
  }, h.empleados, " empleados"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-body)',
      fontVariantNumeric: 'tabular-nums',
      fontSize: 'var(--fs-body)'
    }
  }, h.total), /*#__PURE__*/React.createElement("span", {
    style: {
      justifySelf: 'end'
    }
  }, h.estado === 'ok' ? /*#__PURE__*/React.createElement(Badge, {
    status: "ok"
  }, "Conciliado") : /*#__PURE__*/React.createElement(Badge, {
    status: "review"
  }, "Con ajustes"))))))))), /*#__PURE__*/React.createElement("footer", {
    style: {
      borderTop: '1px solid var(--border-default)',
      background: 'var(--quick-white)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--page-max)',
      margin: '0 auto',
      padding: '18px var(--space-5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/quick-logo.png",
    alt: "Quick",
    style: {
      height: 22
    }
  }), "Herramienta interna de liquidaci\xF3n \xB7 Quick Log\xEDstica S.A.S."), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-micro)',
      color: 'var(--text-subtle)'
    }
  }, "v2.4 \xB7 Datos de ejemplo"))));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(PayrollScreen, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/liquidacion/PayrollScreen.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Header = __ds_scope.Header;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Expander = __ds_scope.Expander;

__ds_ns.MetricTile = __ds_scope.MetricTile;

__ds_ns.DataTable = __ds_scope.DataTable;

__ds_ns.AlertPanel = __ds_scope.AlertPanel;

__ds_ns.FileDropzone = __ds_scope.FileDropzone;

})();
