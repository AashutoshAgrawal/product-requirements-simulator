declare module 'jspdf' {
  export class jsPDF {
    constructor(options?: { orientation?: 'p' | 'l'; unit?: string; format?: string });
    setFont(font: string | undefined, style?: string): this;
    setFontSize(size: number): this;
    setTextColor(r: number, g: number, b: number): this;
    text(text: string, x: number, y: number, options?: { maxWidth?: number }): this;
    setLineHeightFactor(value: number): this;
    addPage(format?: string, orientation?: 'p' | 'l'): this;
    save(filename: string, options?: { returnBlob?: boolean }): void;
    output(type: 'blob' | 'arraybuffer' | 'dataurlstring'): Blob | ArrayBuffer | string;
  }
}
