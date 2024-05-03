// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/bar-chart
function GroupedBarChart(data, {
    x = (d, i) => i, // given d in data, returns the (ordinal) x-value
    y = d => d, // given d in data, returns the (quantitative) y-value
    z = () => 1, // given d in data, returns the (categorical) z-value
    title, // given d in data, returns the title text
    marginTop = 30, // top margin, in pixels
    marginRight = 0, // right margin, in pixels
    marginBottom = 30, // bottom margin, in pixels
    marginLeft = 40, // left margin, in pixels
    width = 640, // outer width, in pixels
    height = 400, // outer height, in pixels
    xDomain, // array of x-values
    xRange = [marginLeft, width - marginRight], // [xmin, xmax]
    xPadding = 0.1, // amount of x-range to reserve to separate groups
    yType = d3.scaleLinear, // type of y-scale
    yDomain, // [ymin, ymax]
    yRange = [height - marginBottom, marginTop], // [ymin, ymax]
    zDomain, // array of z-values
    zPadding = 0.05, // amount of x-range to reserve to separate bars
    yFormat, // a format specifier string for the y-axis
    yLabel, // a label for the y-axis
    colors = d3.schemeTableau10, // array of colors
    numeric_x=false
} = {}) {
    // Compute values.
    const X = d3.map(data, x);
    const Y = d3.map(data, y);
    const Z = d3.map(data, z);

    // Compute default domains, and unique the x- and z-domains.
    if (xDomain === undefined) xDomain = X;
    if (yDomain === undefined) yDomain = [0, d3.max(Y)];
    if (zDomain === undefined) zDomain = Z;
    xDomain = new d3.InternSet(xDomain);
    zDomain = new d3.InternSet(zDomain);

    // Omit any data not present in both the x- and z-domain.
    const I = d3.range(X.length).filter(i => xDomain.has(X[i]) && zDomain.has(Z[i]));

    // Construct scales, axes, and formats.
    const xScale = d3.scaleBand(xDomain, xRange).paddingInner(xPadding);
    const xzScale = d3.scaleBand(zDomain, [0, xScale.bandwidth()]).padding(zPadding);
    const yScale = yType(yDomain, yRange);
    const zScale = d3.scaleOrdinal(zDomain, colors);
    const xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
    const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);
    // var xAxis=null;
    // // const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);
    // if (numeric_x) {
    //     const xAxisTicks = xScale.ticks()
    //         .filter(tick => Number.isInteger(tick));
    //     xAxis = d3.axisLeft(xScale)
    //         .tickValues(xAxisTicks)
    //         .tickFormat(d3.format('d'));
    // } else {
    //     xAxis = d3.axisBottom(xScale).ticks(width / 80).tickSizeOuter(0);
    // }
    // Compute titles.
    if (title === undefined) {
        const formatValue = yScale.tickFormat(100, yFormat);
        title = i => `${X[i]}\n${Z[i]}\n${formatValue(Y[i])}`;
    } else {
        const O = d3.map(data, d => d);
        const T = title;
        title = i => T(O[i], i, data);
    }

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis)
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(yLabel));

    const bar = svg.append("g")
        .selectAll("rect")
        .data(I)
        .join("rect")
        .attr("x", i => xScale(X[i]) + xzScale(Z[i]))
        .attr("y", i => yScale(Y[i]))
        .attr("width", xzScale.bandwidth())
        .attr("height", i => yScale(0) - yScale(Y[i]))
        .attr("fill", i => zScale(Z[i]));

    if (title) bar.append("title")
        .text(title);

    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis);

    return Object.assign(svg.node(), {scales: {color: zScale}});
}


// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/bar-chart
function BarChart(data, {
    x = (d, i) => i, // given d in data, returns the (ordinal) x-value
    y = d => d, // given d in data, returns the (quantitative) y-value
    title, // given d in data, returns the title text
    marginTop = 20, // the top margin, in pixels
    marginRight = 0, // the right margin, in pixels
    marginBottom = 30, // the bottom margin, in pixels
    marginLeft = 40, // the left margin, in pixels
    width = 640, // the outer width of the chart, in pixels
    height = 400, // the outer height of the chart, in pixels
    xDomain, // an array of (ordinal) x-values
    xRange = [marginLeft, width - marginRight], // [left, right]
    yType = d3.scaleLinear, // y-scale type
    yDomain, // [ymin, ymax]
    yRange = [height - marginBottom, marginTop], // [bottom, top]
    xPadding = 0.1, // amount of x-range to reserve to separate bars
    yFormat, // a format specifier string for the y-axis
    yLabel, // a label for the y-axis
    color = "currentColor" // bar fill color
} = {}) {
    // Compute values.
    const X = d3.map(data, x);
    const Y = d3.map(data, y);

    // Compute default domains, and unique the x-domain.
    if (xDomain === undefined) xDomain = X;
    if (yDomain === undefined) yDomain = [0, d3.max(Y)];
    xDomain = new d3.InternSet(xDomain);

    // Omit any data not present in the x-domain.
    const I = d3.range(X.length).filter(i => xDomain.has(X[i]));

    // Construct scales, axes, and formats.
    const xScale = d3.scaleBand(xDomain, xRange).padding(xPadding);
    const yScale = yType(yDomain, yRange);
    const xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
    const yAxis = d3.axisLeft(yScale).ticks(height / 40, yFormat);

    // Compute titles.
    if (title === undefined) {
        const formatValue = yScale.tickFormat(100, yFormat);
        title = i => `${X[i]}\n${formatValue(Y[i])}`;
    } else {
        const O = d3.map(data, d => d);
        const T = title;
        title = i => T(O[i], i, data);
    }

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis)
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(yLabel));

    const bar = svg.append("g")
        .attr("fill", color)
        .selectAll("rect")
        .data(I)
        .join("rect")
        .attr("x", i => xScale(X[i]))
        .attr("y", i => yScale(Y[i]))
        .attr("height", i => yScale(0) - yScale(Y[i]))
        .attr("width", xScale.bandwidth());

    if (title) bar.append("title")
        .text(title);

    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis);

    return svg.node();
}


function Legend(color, {
    title,
    tickSize = 6,
    width = 320,
    height = 44 + tickSize,
    marginTop = 18,
    marginRight = 0,
    marginBottom = 16 + tickSize,
    marginLeft = 0,
    ticks = width / 64,
    tickFormat,
    tickValues
} = {}) {

    function ramp(color, n = 256) {
        const canvas = document.createElement("canvas");
        canvas.width = n;
        canvas.height = 1;
        const context = canvas.getContext("2d");
        for (let i = 0; i < n; ++i) {
            context.fillStyle = color(i / (n - 1));
            context.fillRect(i, 0, 1, 1);
        }
        return canvas;
    }

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("overflow", "visible")
        .style("display", "block");

    let tickAdjust = g => g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);
    let x;

    // Continuous
    if (color.interpolate) {
        const n = Math.min(color.domain().length, color.range().length);

        x = color.copy().rangeRound(d3.quantize(d3.interpolate(marginLeft, width - marginRight), n));

        svg.append("image")
            .attr("x", marginLeft)
            .attr("y", marginTop)
            .attr("width", width - marginLeft - marginRight)
            .attr("height", height - marginTop - marginBottom)
            .attr("preserveAspectRatio", "none")
            .attr("xlink:href", ramp(color.copy().domain(d3.quantize(d3.interpolate(0, 1), n))).toDataURL());
    }

    // Sequential
    else if (color.interpolator) {
        x = Object.assign(color.copy()
                .interpolator(d3.interpolateRound(marginLeft, width - marginRight)),
            {
                range() {
                    return [marginLeft, width - marginRight];
                }
            });

        svg.append("image")
            .attr("x", marginLeft)
            .attr("y", marginTop)
            .attr("width", width - marginLeft - marginRight)
            .attr("height", height - marginTop - marginBottom)
            .attr("preserveAspectRatio", "none")
            .attr("xlink:href", ramp(color.interpolator()).toDataURL());

        // scaleSequentialQuantile doesn’t implement ticks or tickFormat.
        if (!x.ticks) {
            if (tickValues === undefined) {
                const n = Math.round(ticks + 1);
                tickValues = d3.range(n).map(i => d3.quantile(color.domain(), i / (n - 1)));
            }
            if (typeof tickFormat !== "function") {
                tickFormat = d3.format(tickFormat === undefined ? ",f" : tickFormat);
            }
        }
    }

    // Threshold
    else if (color.invertExtent) {
        const thresholds
            = color.thresholds ? color.thresholds() // scaleQuantize
            : color.quantiles ? color.quantiles() // scaleQuantile
                : color.domain(); // scaleThreshold

        const thresholdFormat
            = tickFormat === undefined ? d => d
            : typeof tickFormat === "string" ? d3.format(tickFormat)
                : tickFormat;

        x = d3.scaleLinear()
            .domain([-1, color.range().length - 1])
            .rangeRound([marginLeft, width - marginRight]);

        svg.append("g")
            .selectAll("rect")
            .data(color.range())
            .join("rect")
            .attr("x", (d, i) => x(i - 1))
            .attr("y", marginTop)
            .attr("width", (d, i) => x(i) - x(i - 1))
            .attr("height", height - marginTop - marginBottom)
            .attr("fill", d => d);

        tickValues = d3.range(thresholds.length);
        tickFormat = i => thresholdFormat(thresholds[i], i);
    }

    // Ordinal
    else {
        x = d3.scaleBand()
            .domain(color.domain())
            .rangeRound([marginLeft, width - marginRight]);

        svg.append("g")
            .selectAll("rect")
            .data(color.domain())
            .join("rect")
            .attr("x", x)
            .attr("y", marginTop)
            .attr("width", Math.max(0, x.bandwidth() - 1))
            .attr("height", height - marginTop - marginBottom)
            .attr("fill", color);

        tickAdjust = () => {
        };
    }

    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x)
            .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
            .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
            .tickSize(tickSize)
            .tickValues(tickValues))
        .call(tickAdjust)
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
            .attr("x", marginLeft)
            .attr("y", marginTop + marginBottom - height - 6)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .attr("class", "title")
            .text(title));

    return svg.node();
}


// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/multi-line-chart
function LineChart(data, {
    x = ([x]) => x, // given d in data, returns the (temporal) x-value
    y = ([, y]) => y, // given d in data, returns the (quantitative) y-value
    z = () => 1, // given d in data, returns the (categorical) z-value
    title, // given d in data, returns the title text
    defined, // for gaps in data
    curve = d3.curveLinear, // method of interpolation between points
    marginTop = 20, // top margin, in pixels
    marginRight = 30, // right margin, in pixels
    marginBottom = 30, // bottom margin, in pixels
    marginLeft = 40, // left margin, in pixels
    width = 640, // outer width, in pixels
    height = 400, // outer height, in pixels
    xType = d3.scaleUtc, // type of x-scale
    xDomain, // [xmin, xmax]
    xRange = [marginLeft, width - marginRight], // [left, right]
    yType = d3.scaleLinear, // type of y-scale
    yDomain, // [ymin, ymax]
    yRange = [height - marginBottom, marginTop], // [bottom, top]
    yFormat, // a format specifier string for the y-axis
    yLabel, // a label for the y-axis
    zDomain, // array of z-values
    color = "currentColor", // stroke color of line, as a constant or a function of *z*
    strokeLinecap, // stroke line cap of line
    strokeLinejoin, // stroke line join of line
    strokeWidth = 1.5, // stroke width of line
    strokeOpacity, // stroke opacity of line
    mixBlendMode = "multiply", // blend mode of lines
    voronoi, // show a Voronoi overlay? (for debugging),
    numeric_x=false
} = {}) {
    // Compute values.
    const X = d3.map(data, x);
    const Y = d3.map(data, y);
    const Z = d3.map(data, z);
    const O = d3.map(data, d => d);
    if (defined === undefined) defined = (d, i) => !isNaN(X[i]) && !isNaN(Y[i]);
    const D = d3.map(data, defined);

    // Compute default domains, and unique the z-domain.
    if (xDomain === undefined) xDomain = d3.extent(X);
    if (yDomain === undefined) yDomain = [d3.min(Y), d3.max(Y)]; //change 0 as min to d3.min(Y) to set minimum values
    if (zDomain === undefined) zDomain = Z;
    zDomain = new d3.InternSet(zDomain);

    // Omit any data not present in the z-domain.
    const I = d3.range(X.length).filter(i => zDomain.has(Z[i]));

    // Construct scales and axes.
    const xScale = xType(xDomain, xRange);
    const yScale = yType(yDomain, yRange);
    // const xAxis = d3.axisBottom(xScale).ticks(width / 80).tickSizeOuter(0);
    // const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);
 const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);
    var xAxis=null;
    // const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);
    if (numeric_x) {
        const xAxisTicks = xScale.ticks()
            .filter(tick => Number.isInteger(tick));
        xAxis = d3.axisBottom(xScale).ticks(width / 80).tickSizeOuter(0)
            .tickValues(xAxisTicks)
            .tickFormat(d3.format('d'));
    } else {
        xAxis = d3.axisBottom(xScale).ticks(width / 80).tickSizeOuter(0);
    }
    // Compute titles.
    const T = title === undefined ? Z : title === null ? null : d3.map(data, title);

    // Construct a line generator.
    const line = d3.line()
        .defined(i => D[i])
        .curve(curve)
        .x(i => xScale(X[i]))
        .y(i => yScale(Y[i]));

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
        .style("-webkit-tap-highlight-color", "transparent")
        .on("pointerenter", pointerentered)
        .on("pointermove", pointermoved)
        .on("pointerleave", pointerleft)
        .on("touchstart", event => event.preventDefault());

    // An optional Voronoi display (for fun).
    if (voronoi) svg.append("path")
        .attr("fill", "none")
        .attr("stroke", "#ccc")
        .attr("d", d3.Delaunay
            .from(I, i => xScale(X[i]), i => yScale(Y[i]))
            .voronoi([0, 0, width, height])
            .render());

    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis);

    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis)
        .call(g => g.select(".domain").remove())
        .call(voronoi ? () => {
        } : g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(yLabel));

    const path = svg.append("g")
        .attr("fill", "none")
        .attr("stroke", typeof color === "string" ? color : null)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-linejoin", strokeLinejoin)
        .attr("stroke-width", strokeWidth)
        .attr("stroke-opacity", strokeOpacity)
        .selectAll("path")
        .data(d3.group(I, i => Z[i]))
        .join("path")
        .style("mix-blend-mode", mixBlendMode)
        .attr("stroke", typeof color === "function" ? ([z]) => color(z) : null)
        .attr("d", ([, I]) => line(I));

    const dot = svg.append("g")
        .attr("display", "none");

    dot.append("circle")
        .attr("r", 2.5);

    dot.append("text")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "middle")
        .attr("y", -8);

    function pointermoved(event) {
        const [xm, ym] = d3.pointer(event);
        const i = d3.least(I, i => Math.hypot(xScale(X[i]) - xm, yScale(Y[i]) - ym)); // closest point
        path.style("stroke", ([z]) => Z[i] === z ? null : "#ddd").filter(([z]) => Z[i] === z).raise();
        dot.attr("transform", `translate(${xScale(X[i])},${yScale(Y[i])})`);
        if (T) dot.select("text").text(T[i]);
        svg.property("value", O[i]).dispatch("input", {bubbles: true});
    }

    function pointerentered() {
        path.style("mix-blend-mode", null).style("stroke", "#ddd");
        dot.attr("display", null);
    }

    function pointerleft() {
        path.style("mix-blend-mode", "multiply").style("stroke", null);
        dot.attr("display", "none");
        svg.node().value = null;
        svg.dispatch("input", {bubbles: true});
    }

    return Object.assign(svg.node(), {value: null});
}

// https://github.com/observablehq/htl v0.3.1 Copyright 2019-2021 Observable, Inc.
!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define.amd ? define(["exports"], t) : t((e = "undefined" != typeof globalThis ? globalThis : e || self).htl = {})
}(this, (function (e) {
    "use strict";

    function t(e) {
        const t = document.createElement("template");
        return t.innerHTML = e, document.importNode(t.content, !0)
    }

    function n(e) {
        const t = document.createElementNS("http://www.w3.org/2000/svg", "g");
        return t.innerHTML = e, t
    }

    const r = Object.assign(T(t, (e => {
            if (null === e.firstChild) return null;
            if (e.firstChild === e.lastChild) return e.removeChild(e.firstChild);
            const t = document.createElement("span");
            return t.appendChild(e), t
        })), {fragment: T(t, (e => e))}),
        a = Object.assign(T(n, (e => null === e.firstChild ? null : e.firstChild === e.lastChild ? e.removeChild(e.firstChild) : e)), {
            fragment: T(n, (e => {
                const t = document.createDocumentFragment();
                for (; e.firstChild;) t.appendChild(e.firstChild);
                return t
            }))
        }), s = 60, i = 62, o = 47, c = 45, l = 33, f = 61, u = 10, d = 11, p = 12, b = 13, h = 14, k = 17, g = 22,
        m = 23, w = 26, x = "http://www.w3.org/2000/svg", C = "http://www.w3.org/1999/xlink",
        y = "http://www.w3.org/XML/1998/namespace", v = "http://www.w3.org/2000/xmlns/",
        A = new Map(["attributeName", "attributeType", "baseFrequency", "baseProfile", "calcMode", "clipPathUnits", "diffuseConstant", "edgeMode", "filterUnits", "glyphRef", "gradientTransform", "gradientUnits", "kernelMatrix", "kernelUnitLength", "keyPoints", "keySplines", "keyTimes", "lengthAdjust", "limitingConeAngle", "markerHeight", "markerUnits", "markerWidth", "maskContentUnits", "maskUnits", "numOctaves", "pathLength", "patternContentUnits", "patternTransform", "patternUnits", "pointsAtX", "pointsAtY", "pointsAtZ", "preserveAlpha", "preserveAspectRatio", "primitiveUnits", "refX", "refY", "repeatCount", "repeatDur", "requiredExtensions", "requiredFeatures", "specularConstant", "specularExponent", "spreadMethod", "startOffset", "stdDeviation", "stitchTiles", "surfaceScale", "systemLanguage", "tableValues", "targetX", "targetY", "textLength", "viewBox", "viewTarget", "xChannelSelector", "yChannelSelector", "zoomAndPan"].map((e => [e.toLowerCase(), e]))),
        N = new Map([["xlink:actuate", C], ["xlink:arcrole", C], ["xlink:href", C], ["xlink:role", C], ["xlink:show", C], ["xlink:title", C], ["xlink:type", C], ["xml:lang", y], ["xml:space", y], ["xmlns", v], ["xmlns:xlink", v]]);

    function T(e, t) {
        return function ({raw: n}) {
            let r, a, x, C, y = 1, v = "", A = 0;
            for (let e = 0, t = arguments.length; e < t; ++e) {
                const t = n[e];
                if (e > 0) {
                    const r = arguments[e];
                    switch (y) {
                        case w:
                            if (null != r) {
                                const e = `${r}`;
                                if (E(a)) v += e.replace(/[<]/g, L); else {
                                    if (new RegExp(`</${a}[\\s>/]`, "i").test(v.slice(-a.length - 2) + e)) throw new Error("unsafe raw text");
                                    v += e
                                }
                            }
                            break;
                        case 1:
                            null == r || (r instanceof Node || "string" != typeof r && r[Symbol.iterator] || /(?:^|>)$/.test(n[e - 1]) && /^(?:<|$)/.test(t) ? (v += "\x3c!--::" + e + "--\x3e", A |= 128) : v += `${r}`.replace(/[<&]/g, L));
                            break;
                        case 9: {
                            let a;
                            if (y = p, /^[\s>]/.test(t)) {
                                if (null == r || !1 === r) {
                                    v = v.slice(0, x - n[e - 1].length);
                                    break
                                }
                                if (!0 === r || "" == (a = `${r}`)) {
                                    v += "''";
                                    break
                                }
                                if ("style" === n[e - 1].slice(x, C) && M(r) || "function" == typeof r) {
                                    v += "::" + e, A |= 1;
                                    break
                                }
                            }
                            if (void 0 === a && (a = `${r}`), "" === a) throw new Error("unsafe unquoted empty string");
                            v += a.replace(/^['"]|[\s>&]/g, L);
                            break
                        }
                        case p:
                            v += `${r}`.replace(/[\s>&]/g, L);
                            break;
                        case d:
                            v += `${r}`.replace(/['&]/g, L);
                            break;
                        case u:
                            v += `${r}`.replace(/["&]/g, L);
                            break;
                        case 6:
                            if (M(r)) {
                                v += "::" + e + "=''", A |= 1;
                                break
                            }
                            throw new Error("invalid binding");
                        case k:
                            break;
                        default:
                            throw new Error("invalid binding")
                    }
                }
                for (let e = 0, n = t.length; e < n; ++e) {
                    const n = t.charCodeAt(e);
                    switch (y) {
                        case 1:
                            n === s && (y = 2);
                            break;
                        case 2:
                            n === l ? y = 25 : n === o ? y = 3 : S(n) ? (r = e, a = void 0, y = 4, --e) : 63 === n ? (y = 5, --e) : (y = 1, --e);
                            break;
                        case 3:
                            S(n) ? (y = 4, --e) : n === i ? y = 1 : (y = 5, --e);
                            break;
                        case 4:
                            U(n) ? (y = 6, a = j(t, r, e)) : n === o ? y = h : n === i && (a = j(t, r, e), y = $(a) ? w : 1);
                            break;
                        case 6:
                            U(n) || (n === o || n === i ? (y = 7, --e) : n === f ? (y = 8, x = e + 1, C = void 0) : (y = 8, --e, x = e + 1, C = void 0));
                            break;
                        case 8:
                            U(n) || n === o || n === i ? (y = 7, --e, C = e) : n === f && (y = 9, C = e);
                            break;
                        case 7:
                            U(n) || (n === o ? y = h : n === f ? y = 9 : n === i ? y = $(a) ? w : 1 : (y = 8, --e, x = e + 1, C = void 0));
                            break;
                        case 9:
                            U(n) || (34 === n ? y = u : 39 === n ? y = d : n === i ? y = $(a) ? w : 1 : (y = p, --e));
                            break;
                        case u:
                            34 === n && (y = b);
                            break;
                        case d:
                            39 === n && (y = b);
                            break;
                        case p:
                            U(n) ? y = 6 : n === i && (y = $(a) ? w : 1);
                            break;
                        case b:
                            U(n) ? y = 6 : n === o ? y = h : n === i ? y = $(a) ? w : 1 : (y = 6, --e);
                            break;
                        case h:
                            n === i ? y = 1 : (y = 6, --e);
                            break;
                        case 5:
                            n === i && (y = 1);
                            break;
                        case 15:
                            n === c ? y = 16 : n === i ? y = 1 : (y = k, --e);
                            break;
                        case 16:
                            n === c ? y = m : n === i ? y = 1 : (y = k, --e);
                            break;
                        case k:
                            n === s ? y = 18 : n === c && (y = g);
                            break;
                        case 18:
                            n === l ? y = 19 : n !== s && (y = k, --e);
                            break;
                        case 19:
                            n === c ? y = 20 : (y = k, --e);
                            break;
                        case 20:
                            n === c ? y = 21 : (y = m, --e);
                            break;
                        case 21:
                            y = m, --e;
                            break;
                        case g:
                            n === c ? y = m : (y = k, --e);
                            break;
                        case m:
                            n === i ? y = 1 : n === l ? y = 24 : n !== c && (y = k, --e);
                            break;
                        case 24:
                            n === c ? y = g : n === i ? y = 1 : (y = k, --e);
                            break;
                        case 25:
                            n === c && t.charCodeAt(e + 1) === c ? (y = 15, ++e) : (y = 5, --e);
                            break;
                        case w:
                            n === s && (y = 27);
                            break;
                        case 27:
                            n === o ? y = 28 : (y = w, --e);
                            break;
                        case 28:
                            S(n) ? (r = e, y = 29, --e) : (y = w, --e);
                            break;
                        case 29:
                            U(n) && a === j(t, r, e) ? y = 6 : n === o && a === j(t, r, e) ? y = h : n === i && a === j(t, r, e) ? y = 1 : S(n) || (y = w, --e);
                            break;
                        default:
                            y = void 0
                    }
                }
                v += t
            }
            const N = e(v), T = document.createTreeWalker(N, A, null, !1), R = [];
            for (; T.nextNode();) {
                const e = T.currentNode;
                switch (e.nodeType) {
                    case 1: {
                        const t = e.attributes;
                        for (let n = 0, r = t.length; n < r; ++n) {
                            const {name: a, value: s} = t[n];
                            if (/^::/.test(a)) {
                                const t = arguments[+a.slice(2)];
                                P(e, a), --n, --r;
                                for (const n in t) {
                                    const r = t[n];
                                    null == r || !1 === r || ("function" == typeof r ? e[n] = r : "style" === n && M(r) ? B(e[n], r) : O(e, n, !0 === r ? "" : r))
                                }
                            } else if (/^::/.test(s)) {
                                const t = arguments[+s.slice(2)];
                                P(e, a), --n, --r, "function" == typeof t ? e[a] = t : B(e[a], t)
                            }
                        }
                        break
                    }
                    case 8:
                        if (/^::/.test(e.data)) {
                            const t = e.parentNode, n = arguments[+e.data.slice(2)];
                            if (n instanceof Node) t.insertBefore(n, e); else if ("string" != typeof n && n[Symbol.iterator]) if (n instanceof NodeList || n instanceof HTMLCollection) for (let r = n.length - 1, a = e; r >= 0; --r) a = t.insertBefore(n[r], a); else for (const r of n) null != r && t.insertBefore(r instanceof Node ? r : document.createTextNode(r), e); else t.insertBefore(document.createTextNode(n), e);
                            R.push(e)
                        }
                }
            }
            for (const e of R) e.parentNode.removeChild(e);
            return t(N)
        }
    }

    function L(e) {
        return `&#${e.charCodeAt(0).toString()};`
    }

    function S(e) {
        return 65 <= e && e <= 90 || 97 <= e && e <= 122
    }

    function U(e) {
        return 9 === e || 10 === e || 12 === e || 32 === e || 13 === e
    }

    function M(e) {
        return e && e.toString === Object.prototype.toString
    }

    function $(e) {
        return "script" === e || "style" === e || E(e)
    }

    function E(e) {
        return "textarea" === e || "title" === e
    }

    function j(e, t, n) {
        return e.slice(t, n).toLowerCase()
    }

    function O(e, t, n) {
        e.namespaceURI === x && (t = t.toLowerCase(), t = A.get(t) || t, N.has(t)) ? e.setAttributeNS(N.get(t), t, n) : e.setAttribute(t, n)
    }

    function P(e, t) {
        e.namespaceURI === x && (t = t.toLowerCase(), t = A.get(t) || t, N.has(t)) ? e.removeAttributeNS(N.get(t), t) : e.removeAttribute(t)
    }

    function B(e, t) {
        for (const n in t) {
            const r = t[n];
            n.startsWith("--") ? e.setProperty(n, r) : e[n] = r
        }
    }

    e.html = r, e.svg = a, e.version = "0.3.1", Object.defineProperty(e, "__esModule", {value: !0})
}));

// Copyright 2021, Observable Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/color-legend
function Swatches(color, {
    columns = null,
    format,
    unknown: formatUnknown,
    swatchSize = 15,
    swatchWidth = swatchSize,
    swatchHeight = swatchSize,
    marginLeft = 0
} = {}) {
    const id = `-swatches-${Math.random().toString(16).slice(2)}`;
    const unknown = formatUnknown == null ? undefined : color.unknown();
    const unknowns = unknown == null || unknown === d3.scaleImplicit ? [] : [unknown];
    const domain = color.domain().concat(unknowns);
    if (format === undefined) format = x => x === unknown ? formatUnknown : x;

    function entity(character) {
        return `&#${character.charCodeAt(0).toString()};`;
    }

    if (columns !== null) return htl.html`<div style="display: flex; align-items: center; margin-left: ${+marginLeft}px; min-height: 33px; font: 10px sans-serif;">
  <style>

.${id}-item {
  break-inside: avoid;
  display: flex;
  align-items: center;
  padding-bottom: 1px;
}

.${id}-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: calc(100% - ${+swatchWidth}px - 0.5em);
}

.${id}-swatch {
  width: ${+swatchWidth}px;
  height: ${+swatchHeight}px;
  margin: 0 0.5em 0 0;
}

  </style>
  <div style=${{width: "100%", columns}}>${domain.map(value => {
        const label = `${format(value)}`;
        return htl.html`<div class=${id}-item>
      <div class=${id}-swatch style=${{background: color(value)}}></div>
      <div class=${id}-label title=${label}>${label}</div>
    </div>`;
    })}
  </div>
</div>`;

    return htl.html`<div style="display: flex; align-items: center; min-height: 33px; margin-left: ${+marginLeft}px; font: 10px sans-serif;">
  <style>

.${id} {
  display: inline-flex;
  align-items: center;
  margin-right: 1em;
}

.${id}::before {
  content: "";
  width: ${+swatchWidth}px;
  height: ${+swatchHeight}px;
  margin-right: 0.5em;
  background: var(--color);
}

  </style>
  <div style="text-align: center">${domain.map(value => htl.html`<span class="${id}" style="--color: ${color(value)}">${format(value)}</span>`)}</div>`;
}


function LineGraphWithCheckbox(data) {


    var margin = {top: 20, right: 200, bottom: 100, left: 50},
        margin2 = {top: 430, right: 10, bottom: 20, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        height2 = 500 - margin2.top - margin2.bottom;

    var parseDate = d3.time.format("%Y%m%d").parse;
    var bisectDate = d3.bisector(function (d) {
        return d.date;
    }).left;

    var xScale = d3.time.scale()
            .range([0, width]),

        xScale2 = d3.time.scale()
            .range([0, width]); // Duplicate xScale for brushing ref later

    var yScale = d3.scale.linear()
        .range([height, 0]);

// 40 Custom DDV colors
    var color = d3.scale.ordinal().range(["#48A36D", "#56AE7C", "#64B98C", "#72C39B", "#80CEAA", "#80CCB3", "#7FC9BD", "#7FC7C6", "#7EC4CF", "#7FBBCF", "#7FB1CF", "#80A8CE", "#809ECE", "#8897CE", "#8F90CD", "#9788CD", "#9E81CC", "#AA81C5", "#B681BE", "#C280B7", "#CE80B0", "#D3779F", "#D76D8F", "#DC647E", "#E05A6D", "#E16167", "#E26962", "#E2705C", "#E37756", "#E38457", "#E39158", "#E29D58", "#E2AA59", "#E0B15B", "#DFB95C", "#DDC05E", "#DBC75F", "#E3CF6D", "#EAD67C", "#F2DE8A"]);


    var xAxis = d3.svg.axis()
            .scale(xScale)
            .orient("bottom"),

        xAxis2 = d3.svg.axis() // xAxis for brush slider
            .scale(xScale2)
            .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("basis")
        .x(function (d) {
            return xScale(d.date);
        })
        .y(function (d) {
            return yScale(d.rating);
        })
        .defined(function (d) {
            return d.rating;
        });  // Hiding line value defaults of 0 for missing data

    var maxY; // Defined later to update yAxis

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom) //height + margin.top + margin.bottom
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Create invisible rect for mouse tracking
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .attr("x", 0)
        .attr("y", 0)
        .attr("id", "mouse-tracker")
        .style("fill", "white");

//for slider part-----------------------------------------------------------------------------------

    var context = svg.append("g") // Brushing context box container
        .attr("transform", "translate(" + 0 + "," + 410 + ")")
        .attr("class", "context");

//append clip path for lines plotted, hiding those part out of bounds
    svg.append("defs")
        .append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);

//end slider part-----------------------------------------------------------------------------------


    d3.tsv("data.tsv", function (error, data) {
        color.domain(d3.keys(data[0]).filter(function (key) { // Set the domain of the color ordinal scale to be all the csv headers except "date", matching a color to an issue
            return key !== "date";
        }));

        data.forEach(function (d) { // Make every date in the csv data a javascript date object format
            d.date = parseDate(d.date);
        });

        var categories = color.domain().map(function (name) { // Nest the data into an array of objects with new keys

            return {
                name: name, // "name": the csv headers except date
                values: data.map(function (d) { // "values": which has an array of the dates and ratings
                    return {
                        date: d.date,
                        rating: +(d[name]),
                    };
                }),
                visible: (name === "Unemployment" ? true : false) // "visible": all false except for economy which is true.
            };
        });

        xScale.domain(d3.extent(data, function (d) {
            return d.date;
        })); // extent = highest and lowest points, domain is data, range is bouding box

        yScale.domain([0, 100
            //d3.max(categories, function(c) { return d3.max(c.values, function(v) { return v.rating; }); })
        ]);

        xScale2.domain(xScale.domain()); // Setting a duplicate xdomain for brushing reference later

        //for slider part-----------------------------------------------------------------------------------

        var brush = d3.svg.brush()//for slider bar at the bottom
            .x(xScale2)
            .on("brush", brushed);

        context.append("g") // Create brushing xAxis
            .attr("class", "x axis1")
            .attr("transform", "translate(0," + height2 + ")")
            .call(xAxis2);

        var contextArea = d3.svg.area() // Set attributes for area chart in brushing context graph
            .interpolate("monotone")
            .x(function (d) {
                return xScale2(d.date);
            }) // x is scaled to xScale2
            .y0(height2) // Bottom line begins at height2 (area chart not inverted)
            .y1(0); // Top line of area, 0 (area chart not inverted)

        //plot the rect as the bar at the bottom
        context.append("path") // Path is created using svg.area details
            .attr("class", "area")
            .attr("d", contextArea(categories[0].values)) // pass first categories data .values to area path generator
            .attr("fill", "#F1F1F2");

        //append the brush for the selection of subsection
        context.append("g")
            .attr("class", "x brush")
            .call(brush)
            .selectAll("rect")
            .attr("height", height2) // Make brush rects same height
            .attr("fill", "#E6E7E8");
        //end slider part-----------------------------------------------------------------------------------

        // draw line graph
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("x", -10)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Issues Rating");

        var issue = svg.selectAll(".issue")
            .data(categories) // Select nested data and append to new svg group elements
            .enter().append("g")
            .attr("class", "issue");

        issue.append("path")
            .attr("class", "line")
            .style("pointer-events", "none") // Stop line interferring with cursor
            .attr("id", function (d) {
                return "line-" + d.name.replace(" ", "").replace("/", ""); // Give line id of line-(insert issue name, with any spaces replaced with no spaces)
            })
            .attr("d", function (d) {
                return d.visible ? line(d.values) : null; // If array key "visible" = true then draw line, if not then don't
            })
            .attr("clip-path", "url(#clip)")//use clip path to make irrelevant part invisible
            .style("stroke", function (d) {
                return color(d.name);
            });

        // draw legend
        var legendSpace = 450 / categories.length; // 450/number of issues (ex. 40)

        issue.append("rect")
            .attr("width", 10)
            .attr("height", 10)
            .attr("x", width + (margin.right / 3) - 15)
            .attr("y", function (d, i) {
                return (legendSpace) + i * (legendSpace) - 8;
            })  // spacing
            .attr("fill", function (d) {
                return d.visible ? color(d.name) : "#F1F1F2"; // If array key "visible" = true then color rect, if not then make it grey
            })
            .attr("class", "legend-box")

            .on("click", function (d) { // On click make d.visible
                d.visible = !d.visible; // If array key for this data selection is "visible" = true then make it false, if false then make it true

                maxY = findMaxY(categories); // Find max Y rating value categories data with "visible"; true
                yScale.domain([0, maxY]); // Redefine yAxis domain based on highest y value of categories data with "visible"; true
                svg.select(".y.axis")
                    .transition()
                    .call(yAxis);

                issue.select("path")
                    .transition()
                    .attr("d", function (d) {
                        return d.visible ? line(d.values) : null; // If d.visible is true then draw line for this d selection
                    })

                issue.select("rect")
                    .transition()
                    .attr("fill", function (d) {
                        return d.visible ? color(d.name) : "#F1F1F2";
                    });
            })

            .on("mouseover", function (d) {

                d3.select(this)
                    .transition()
                    .attr("fill", function (d) {
                        return color(d.name);
                    });

                d3.select("#line-" + d.name.replace(" ", "").replace("/", ""))
                    .transition()
                    .style("stroke-width", 2.5);
            })

            .on("mouseout", function (d) {

                d3.select(this)
                    .transition()
                    .attr("fill", function (d) {
                        return d.visible ? color(d.name) : "#F1F1F2";
                    });

                d3.select("#line-" + d.name.replace(" ", "").replace("/", ""))
                    .transition()
                    .style("stroke-width", 1.5);
            })

        issue.append("text")
            .attr("x", width + (margin.right / 3))
            .attr("y", function (d, i) {
                return (legendSpace) + i * (legendSpace);
            })  // (return (11.25/2 =) 5.625) + i * (5.625)
            .text(function (d) {
                return d.name;
            });

        // Hover line
        var hoverLineGroup = svg.append("g")
            .attr("class", "hover-line");

        var hoverLine = hoverLineGroup // Create line with basic attributes
            .append("line")
            .attr("id", "hover-line")
            .attr("x1", 10).attr("x2", 10)
            .attr("y1", 0).attr("y2", height + 10)
            .style("pointer-events", "none") // Stop line interferring with cursor
            .style("opacity", 1e-6); // Set opacity to zero

        var hoverDate = hoverLineGroup
            .append('text')
            .attr("class", "hover-text")
            .attr("y", height - (height - 40)) // hover date text position
            .attr("x", width - 150) // hover date text position
            .style("fill", "#E6E7E8");

        var columnNames = d3.keys(data[0]) //grab the key values from your first data row
            //these are the same as your column names
            .slice(1); //remove the first column name (`date`);

        var focus = issue.select("g") // create group elements to house tooltip text
            .data(columnNames) // bind each column name date to each g element
            .enter().append("g") //create one <g> for each columnName
            .attr("class", "focus");

        focus.append("text") // http://stackoverflow.com/questions/22064083/d3-js-multi-series-chart-with-y-value-tracking
            .attr("class", "tooltip")
            .attr("x", width + 20) // position tooltips
            .attr("y", function (d, i) {
                return (legendSpace) + i * (legendSpace);
            }); // (return (11.25/2 =) 5.625) + i * (5.625) // position tooltips

        // Add mouseover events for hover line.
        d3.select("#mouse-tracker") // select chart plot background rect #mouse-tracker
            .on("mousemove", mousemove) // on mousemove activate mousemove function defined below
            .on("mouseout", function () {
                hoverDate
                    .text(null) // on mouseout remove text for hover date

                d3.select("#hover-line")
                    .style("opacity", 1e-6); // On mouse out making line invisible
            });

        function mousemove() {
            var mouse_x = d3.mouse(this)[0]; // Finding mouse x position on rect
            var graph_x = xScale.invert(mouse_x); //

            //var mouse_y = d3.mouse(this)[1]; // Finding mouse y position on rect
            //var graph_y = yScale.invert(mouse_y);
            //console.log(graph_x);

            var format = d3.time.format('%b %Y'); // Format hover date text to show three letter month and full year

            hoverDate.text(format(graph_x)); // scale mouse position to xScale date and format it to show month and year

            d3.select("#hover-line") // select hover-line and changing attributes to mouse position
                .attr("x1", mouse_x)
                .attr("x2", mouse_x)
                .style("opacity", 1); // Making line visible

            // Legend tooltips // http://www.d3noob.org/2014/07/my-favourite-tooltip-method-for-line.html

            var x0 = xScale.invert(d3.mouse(this)[0]), /* d3.mouse(this)[0] returns the x position on the screen of the mouse. xScale.invert function is reversing the process that we use to map the domain (date) to range (position on screen). So it takes the position on the screen and converts it into an equivalent date! */
                i = bisectDate(data, x0, 1), // use our bisectDate function that we declared earlier to find the index of our data array that is close to the mouse cursor
                /*It takes our data array and the date corresponding to the position of or mouse cursor and returns the index number of the data array which has a date that is higher than the cursor position.*/
                d0 = data[i - 1],
                d1 = data[i],
                /*d0 is the combination of date and rating that is in the data array at the index to the left of the cursor and d1 is the combination of date and close that is in the data array at the index to the right of the cursor. In other words we now have two variables that know the value and date above and below the date that corresponds to the position of the cursor.*/
                d = x0 - d0.date > d1.date - x0 ? d1 : d0;
            /*The final line in this segment declares a new array d that is represents the date and close combination that is closest to the cursor. It is using the magic JavaScript short hand for an if statement that is essentially saying if the distance between the mouse cursor and the date and close combination on the left is greater than the distance between the mouse cursor and the date and close combination on the right then d is an array of the date and close on the right of the cursor (d1). Otherwise d is an array of the date and close on the left of the cursor (d0).*/

            //d is now the data row for the date closest to the mouse position

            focus.select("text").text(function (columnName) {
                //because you didn't explictly set any data on the <text>
                //elements, each one inherits the data from the focus <g>

                return (d[columnName]);
            });
        };

        //for brusher of the slider bar at the bottom
        function brushed() {

            xScale.domain(brush.empty() ? xScale2.domain() : brush.extent()); // If brush is empty then reset the Xscale domain to default, if not then make it the brush extent

            svg.select(".x.axis") // replot xAxis with transition when brush used
                .transition()
                .call(xAxis);

            maxY = findMaxY(categories); // Find max Y rating value categories data with "visible"; true
            yScale.domain([0, maxY]); // Redefine yAxis domain based on highest y value of categories data with "visible"; true

            svg.select(".y.axis") // Redraw yAxis
                .transition()
                .call(yAxis);

            issue.select("path") // Redraw lines based on brush xAxis scale and domain
                .transition()
                .attr("d", function (d) {
                    return d.visible ? line(d.values) : null; // If d.visible is true then draw line for this d selection
                });

        };

    }); // End Data callback function

    function findMaxY(data) {  // Define function "findMaxY"
        var maxYValues = data.map(function (d) {
            if (d.visible) {
                return d3.max(d.values, function (value) { // Return max rating value
                    return value.rating;
                })
            }
        });
        return d3.max(maxYValues);
    }
}