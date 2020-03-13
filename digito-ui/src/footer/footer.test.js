import React from 'react';
import {mount, shallow} from "enzyme";

import {FlatLinksList, FooterStateless, VerticalSeparator} from "./footer";
import {Container, Segment} from "semantic-ui-react";

describe("<FooterStateless/>", () => {
  let links = [
    {name: "Link1", href: "/test/link1"},
    {name: "Link2", href: "test/link2"},
    {name: "Link3", href: "test/link3"}
  ];
  it('renders without errors', () => {
    mount(<FooterStateless links={links}/>);
  });
  it('renders without links or logos', () => {
    mount(<FooterStateless links={[]} logos={[]}/>);
  });
  it('forwards links and logos to proper children', () => {
    let result = shallow(<FooterStateless links={links}/>);
    expect(result.find(FlatLinksList).props()).toMatchObject({links: links});
  });
  it('renders centrally aligned', () => {
    let result = shallow(<FooterStateless links={links}/>);
    // I've got absolutely no idea how to test it more appropriately
    expect(result.findWhere(n => n.is(Container) && n.props().textAlign !== "center").getElements().length).toBe(0);
    expect(result.findWhere(n => n.is(Segment) && n.props().textAlign !== "center").getElements().length).toBe(0);
  });
});

describe("<VerticalSeparator/>", () => {
  let separator = "%$£&*^%£$$%";
  it('renders sparse separator by default', () => {
    let result = mount(<VerticalSeparator separator={separator}/>);
    expect(result.find("span").props().children).toBe(` ${separator} `);
  });
  it('renders non-sparse separator if requested', () => {
    let result = mount(<VerticalSeparator separator={separator} sparse={false}/>);
    expect(result.find("span").props().children).toBe(separator);
  });
  it('renders nothing if sparse=false and separator=undefined', () => {
    let result = mount(<VerticalSeparator sparse={false}/>);
    expect(result.find("span").props().children).toBe("");
  });
  it('renders space if sparse=true and separator=undefined', () => {
    let result = mount(<VerticalSeparator sparse={true}/>);
    expect(result.find("span").props().children).toBe(" ");
  });
});

describe("<FlatLinksList/>", () => {
  let separator = "%$£&*^%£$$%";
  it('renders empty list', () => {
    mount(<FlatLinksList links={[]} separator={separator}/>);
  });
  it('renders single link without separator', () => {
    let link = {name: "Test Link", href: "/test/link"};
    let result = mount(<FlatLinksList links={[link]} separator={separator}/>);
    expect(result.find("a").props()).toMatchObject({href: link.href, children: link.name});
    expect(result.find(VerticalSeparator).exists()).toBe(false);
  });
  it('renders multiple links with separators', () => {
    let links = [
      {name: "Test Link 1", href: "/test/link1"},
      {name: "Test Link 2", href: "/test/link2"},
      {name: "Test Link 3", href: "/test/link2"}, // Duplicate links are supported, duplicate names are not
    ];
    let result = mount(<FlatLinksList links={links} separator={separator}/>);
    expect(result.childAt(0).filter('a').props()).toMatchObject({href: links[0].href, children: links[0].name});
    expect(result.childAt(1).props()).toMatchObject({separator: separator});
    expect(result.childAt(2).filter('a').props()).toMatchObject({href: links[1].href, children: links[1].name});
    expect(result.childAt(3).props()).toMatchObject({separator: separator});
    expect(result.childAt(4).filter('a').props()).toMatchObject({href: links[2].href, children: links[2].name});
    expect(result.childAt(5).exists()).toBe(false);
  });
});
