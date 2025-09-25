import { Component, signal } from '@angular/core';
import { CurrencyPipe, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';

import { domain } from './utilities';

@Component({
  selector: 'app-bb-list',
  imports: [CurrencyPipe, DatePipe, RouterLink],
  templateUrl: './bb-list.html',
  styleUrls: ['./bb-list.css']
})
export class BbList {
  protected bbs: any = signal([]);

  async ngOnInit() {
    const result = await fetch(`${domain}bbs/`);
    if (result.ok) {
      const data = await result.json();
      this.bbs.set(data);
    } else 
      window.alert(result.statusText);
  }
}
