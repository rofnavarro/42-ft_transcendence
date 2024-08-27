const { expect } = require("chai");

describe("Token contract", function () {
  it("Deployment should assign the total supply of tokens to the owner", async function () {
    const [owner] = await ethers.getSigners();

    const hardhatTournment = await ethers.deployContract("Tournment");

    const ownerBalance = await hardhatTournment.addMatchData("Hello World");
    expect(await hardhatTournment.getTournments());
  });
});