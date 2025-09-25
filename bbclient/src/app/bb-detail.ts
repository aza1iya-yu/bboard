import { Component, signal, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CurrencyPipe, DatePipe } from '@angular/common';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { Title } from '@angular/platform-browser';

import { domain } from './utilities';

@Component({
  selector: 'app-bb-detail',
  imports: [CurrencyPipe, DatePipe, ReactiveFormsModule],
  templateUrl: './bb-detail.html',
  styleUrls: ['./bb-detail.css']
})
export class BbDetail {
  protected bb: any = signal(undefined);
  protected comments: any = signal([]);

  protected author: any = new FormControl('');
  protected password: any = new FormControl('');
  protected content: any = new FormControl('');

  private route = inject(ActivatedRoute);
  private title = inject(Title);

  async ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    const result = await fetch(`${domain}bbs/${id}/`);
    if (result.ok) {
      const data = await result.json();
      this.bb.set(data);
      this.title.setTitle(data.Title);
      await this.getComments();
    } else 
      window.alert(result.statusText);
  }

  async getComments() {
    const result = await fetch(`${domain}bbs/${this.bb().id}/comments`);
    if (result.ok) {
      const data = await result.json();
      this.comments.set(data);
    } else 
      window.alert(result.statusText);
  }

  async submitComment(evt: Event) {
    evt.preventDefault();
    const comment = { 'bb': this.bb().id, 'author': this.author.value, 'content': this.content.value };
    const result = await fetch(
      `${domain}bbs/${this.bb().id}/comments`,
      {
        method: 'POST',
        body: JSON.stringify(comment),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic' + window.btoa(`${this.author.value}:${this.password.value}`)
        }
      }
    );
    if (result.ok) {
      await this.getComments();
      this.content.setValue('');
    }
  }
}
