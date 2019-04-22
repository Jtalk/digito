import React from 'react';
import * as Enzyme from "enzyme";
import {mount} from "enzyme";
import Adapter from 'enzyme-adapter-react-16';

import VerticalSeparator from "./vertical-separator";

Enzyme.configure({ adapter: new Adapter() });

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
