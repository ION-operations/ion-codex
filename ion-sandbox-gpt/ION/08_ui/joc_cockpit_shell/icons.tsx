import type { SVGProps } from 'react';

const base = {
  width: 16,
  height: 16,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.7,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
};

export function WorkSurfaceIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg>;
}

export function ReceiptIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><path d="M7 3h10v18l-2-1.5-2 1.5-2-1.5-2 1.5-2-1.5z"/><path d="M9 8h6M9 12h6M9 16h3"/></svg>;
}

export function LensIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><circle cx="10.5" cy="10.5" r="5.5"/><path d="m15 15 5 5"/><path d="M8.5 10.5h4"/></svg>;
}

export function StreamIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><path d="M4 7h3l2 10 3-14 2 9h6"/><path d="M4 18h16"/></svg>;
}

export function RouteIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><path d="M5 5h5v5H5zM14 14h5v5h-5z"/><path d="M10 7.5h3.5a3 3 0 0 1 3 3V14"/></svg>;
}

export function GraphIcon(props: SVGProps<SVGSVGElement>) {
  return <svg {...base} {...props}><circle cx="6" cy="7" r="2"/><circle cx="18" cy="7" r="2"/><circle cx="12" cy="17" r="2"/><path d="M8 8l3 7M16 8l-3 7M8 7h8"/></svg>;
}
