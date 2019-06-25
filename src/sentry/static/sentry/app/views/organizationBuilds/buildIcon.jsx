import styled from 'react-emotion';

const getBackgroundColor = p => {
  if (p.color) {
    return `background: ${p.color};`;
  }

  return `background: ${
    p.status === 'needs_approved'
      ? p.theme.error
      : p.status === 'approved'
      ? p.theme.success
      : p.theme.disabled
  };`;
};

const getSize = p => `
  height: ${p.size}px;
  width: ${p.size}px;
`;

export default styled('div')`
  display: inline-block;
  position: relative;
  border-radius: 50%;
  ${getSize};
  ${getBackgroundColor};
`;
