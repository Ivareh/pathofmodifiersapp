import {
  Box,
  CloseButton,
  Flex,
  Input,
  Select,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../Icon/AddIconCheckbox";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../client";
import { useOutsideClick } from "../../hooks/useOutsideClick";
import React from "react";
import { modifiers } from "../../test_data/modifier_data";
// import { GetGroupedModifiersByEffect } from "../../hooks/getGroupedModifiers";

const ModiferInput = () => {
  return <ModifierListInput />;
};

interface ModifierInput extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (string | null)[];
}

function ModifierListInput() {
  const [searchModifierText, setSearchModifierText] = useState("");

  const [filteredModifiers, setFilteredModifiers] = useState<ModifierInput[]>([
    {
      modifierId: [0],
      position: [0],
      effect: "",
    },
  ]);

  const [selectedModifiers, setSelectedModifiers] = useState<ModifierInput[]>(
    []
  );

  const [isExpanded, setIsExpanded] = useState(false);

  // const modifiers: ModifierInput[] | undefined = GetGroupedModifiersByEffect();

  useEffect(() => {
    const testModifiers: ModifierInput[] = modifiers;

    if (testModifiers) {
      const filtered = testModifiers.filter((modifier) =>
        modifier.effect.toLowerCase().includes(searchModifierText.toLowerCase())
      );
      setFilteredModifiers(filtered);
    }
  }, [searchModifierText]);

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
    console.log("Selected modifiers: \n");
    console.log(selectedModifiers);
    console.log("Filtered modifiers: \n");
    console.log(filteredModifiers);
  });

  // Define types for input cases
  type InputCase = "modifier" | "minPosition" | "maxPosition" | "textPosition";

  // Define the function to handle input changes
  const handleInputChange = (
    value: string,
    inputCase: InputCase,
    position?: number,
    modifier?: ModifierInput
  ) => {
    // Regular expression to allow numbers and scientific notation
    // const scientificPattern = /^-?\d*\.?\d*(e-?\d+)?$/i;

    if (inputCase === "modifier") {
      setSearchModifierText(value);
    }
    if (!modifier || position === undefined || position < 0) {
      return;
    }
    switch (inputCase) {
      case "minPosition":
        if (modifier.minRollInputs) {
          modifier.minRollInputs[position] = parseInt(value);
        } else {
          modifier.minRollInputs = [parseInt(value)];
        }
        updateModifierInput(
          modifier.modifierId[position],
          modifier.minRollInputs
        );
        break;
      case "maxPosition":
        if (modifier.maxRollInputs) {
          modifier.maxRollInputs[position] = parseInt(value);
        } else {
          modifier.maxRollInputs = [parseInt(value)];
        }
        updateModifierInput(
          modifier.modifierId[position],
          undefined,
          modifier.maxRollInputs,
          undefined
        );
        break;
      case "textPosition":
        if (modifier.textRollInputs) {
          modifier.textRollInputs[position] = value;
        } else {
          modifier.textRollInputs = [value];
        }
        updateModifierInput(
          modifier.modifierId[position],
          undefined,
          undefined,
          modifier.textRollInputs
        );
        break;
      default:
        // Handle default case
        break;
    }
  };

  const handleModifierSelect = (selectedModifierEffect: ModifierInput) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;
    setSelectedModifiers((prevModifiers) => [
      ...prevModifiers,
      selectedModifierEffect,
    ]);

    if (!isArrayNullOrContainsOnlyNull(selectedModifierEffect.minRoll)) {
      selectedModifierEffect.minRollInputs = [0];
    }
    if (!isArrayNullOrContainsOnlyNull(selectedModifierEffect.maxRoll)) {
      selectedModifierEffect.maxRollInputs = [0];
    }
    if (!isArrayNullOrContainsOnlyNull(selectedModifierEffect.textRolls)) {
      selectedModifierEffect.textRollInputs = [""];
    }

    setSearchModifierText("");
    toggleExpand();
  };

  const handleRemoveModifier = (id: number) => {
    const effectToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId[0] === id
    )?.effect;

    if (effectToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== effectToRemove)
      );
    }
  };

  const handleCheckboxChange = (id: number) => {
    setSelectedModifiers((modifiers) =>
      modifiers.map((modifier) =>
        modifier.modifierId[0] === id
          ? { ...modifier, isSelected: !modifier.isSelected }
          : modifier
      )
    );
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const bottom =
      e.currentTarget.scrollHeight - e.currentTarget.scrollTop ===
      e.currentTarget.clientHeight;
    if (bottom && !isExpanded) {
      setIsExpanded(true);
    }
  };

  const updateModifierInput = (
    modifierId: number,
    newMinRollInputs?: (number | null)[] | undefined,
    newMaxRollInputs?: (number | null)[] | undefined,
    newTextRollInputs?: (string | null)[] | undefined
  ): void => {
    setSelectedModifiers((prevModifiers) => {
      const updatedModifiers = [...prevModifiers]; // Step 1: Create a copy of the array
      const index = updatedModifiers.findIndex(
        (modifier) => modifier.modifierId[0] === modifierId
      ); // Find index based on modifierId
      if (index !== -1) {
        // Ensure modifier with given modifierId exists
        const modifierToUpdate = { ...updatedModifiers[index] }; // Copy the modifier object
        if (newMinRollInputs) {
          modifierToUpdate.minRollInputs = newMinRollInputs; // Update minRollInputs
        } else if (newMaxRollInputs) {
          modifierToUpdate.maxRollInputs = newMaxRollInputs;
        } else if (newTextRollInputs) {
          modifierToUpdate.textRollInputs = newTextRollInputs;
        }
        updatedModifiers[index] = modifierToUpdate; // Replace the old modifier with the updated one
      }
      return updatedModifiers; // Set the updated array back to state
    });
  };

  // Define a function to check if an array has only null values
  function isArrayNullOrContainsOnlyNull<T>(
    arr: T[] | null | undefined
  ): boolean {
    if (arr === null || arr === undefined) {
      return true; // If the array is null, return true
    }
    // Check if every element in the array is null
    return arr.every((value) => value === null);
  }

  interface RenderInputProps {
    modifier: ModifierInput;
    input: string | number | undefined | null;
    handleInputChangeCase: InputCase;
    inputPosition: number;
    width: string;
    placeholder: string;
    key: string;
  }

  const renderInputBasedOnConditions = ({
    modifier,
    input,
    handleInputChangeCase,
    inputPosition,
    width,
    key,
    placeholder,
  }: RenderInputProps): JSX.Element | null => {
    const selectedModifierInput = selectedModifiers.find(
      (selectedModifier) =>
        selectedModifier.modifierId[0] === modifier.modifierId[0]
    );

    if (selectedModifierInput) {
      const handleChange = (
        event:
          | React.ChangeEvent<HTMLInputElement>
          | React.ChangeEvent<HTMLSelectElement>
      ) => {
        const selectedValue = event.target.value;
        // Call function to handle the change
        handleInputChange(
          selectedValue,
          handleInputChangeCase,
          inputPosition,
          modifier
        );
      };

      // Access the specific property of the ModifierInput object based on handleInputChangeCase
      if (
        handleInputChangeCase === "minPosition" ||
        (handleInputChangeCase === "maxPosition" &&
          selectedModifierInput.minRollInputs &&
          selectedModifierInput.maxRollInputs)
      ) {
        let input_value: number | undefined;
        if (input === null && input === undefined) {
          input_value = input;
        }

        return (
          <Input
            value={input_value}
            key={key}
            bgColor={"ui.input"}
            onChange={handleChange}
            width={width}
            placeholder={placeholder}
            _placeholder={{ color: "ui.white" }}
            textAlign={"center"}
          />
        );
      }
      if (
        handleInputChangeCase === "textPosition" &&
        !isArrayNullOrContainsOnlyNull(modifier.textRolls) &&
        modifier.textRolls
      ) {
        const textRolls = modifier.textRolls[inputPosition] as string;
        const textRollsList = textRolls.split("-");

        const textRollsOptions = textRollsList.map((textRoll, index) => (
          <option value={textRoll} key={key + textRoll + index}>
            {textRoll}
          </option>
        ));

        return (
          <Select
            bgColor={"ui.white"}
            color={"ui.dark"}
            defaultValue={"TextRolls"}
            onChange={handleChange}
            width={width}
            key={key}
          >
            {textRollsOptions}
          </Select>
        );
      }
    }
    return null;
  };

  // Render selected modifiers list
  const selectedModifiersList = selectedModifiers.map((modifier, index) => (
    <Flex key={index} alignItems="center" bgColor={"ui.secondary"}>
      <Box bgColor={"ui.main"} width={8} height={8}>
        <AddIconCheckbox
          isChecked={modifier.isSelected}
          top={"24%"}
          left={"24%"}
          key={modifier.modifierId[0]}
          onChange={() => {
            if (modifier.modifierId[0] !== null) {
              handleCheckboxChange(modifier.modifierId[0]);
            }
          }}
        />
      </Box>

      <Text ml={3} mr={"auto"}>
        {modifier.effect}
      </Text>

      <Flex width={"80"} justifyContent="flex-end" ml={"auto"}>
        {/* Check if modifier static exists and is not all null */}
        {isArrayNullOrContainsOnlyNull(modifier.static) &&
          (() => {
            const elements = [];
            for (
              let modifierInputIndex = 0;
              modifierInputIndex < modifier.position.length;
              modifierInputIndex++
            ) {
              const selectedModifier = selectedModifiers.find(
                (selectedModifier) =>
                  selectedModifier.modifierId[0] === modifier.modifierId[0]
              );
              if (
                !isArrayNullOrContainsOnlyNull(modifier.minRoll) &&
                modifier.minRoll &&
                modifier.minRoll[modifierInputIndex] !== null
              ) {
                const selectedModifierInput = selectedModifier?.minRollInputs
                  ? selectedModifier.minRollInputs[modifierInputIndex]
                  : undefined;

                elements.push(
                  renderInputBasedOnConditions({
                    modifier: modifier,
                    input: selectedModifierInput,
                    width: "20",
                    handleInputChangeCase: "minPosition" as InputCase,
                    inputPosition: modifierInputIndex,
                    key: "minPosition" + index + modifierInputIndex,
                    placeholder: "MIN",
                  })
                );
              }

              if (
                !isArrayNullOrContainsOnlyNull(modifier.maxRoll) &&
                modifier.maxRoll &&
                modifier.maxRoll[modifierInputIndex] !== null
              ) {
                const selectedModifierInput = selectedModifier?.maxRollInputs
                  ? selectedModifier.maxRollInputs[modifierInputIndex]
                  : undefined;

                elements.push(
                  renderInputBasedOnConditions({
                    modifier: modifier,
                    input: selectedModifierInput,
                    handleInputChangeCase: "maxPosition" as InputCase,
                    inputPosition: modifierInputIndex,
                    width: "20",
                    key: "maxPosition" + index + modifierInputIndex,
                    placeholder: "MAX",
                  })
                );
              }
              if (
                !isArrayNullOrContainsOnlyNull(modifier.textRolls) &&
                modifier.textRolls &&
                modifier.textRolls[modifierInputIndex] !== null
              ) {
                const selectedModifierInput = selectedModifier?.textRollInputs
                  ? selectedModifier.textRollInputs[modifierInputIndex]
                  : undefined;

                elements.push(
                  renderInputBasedOnConditions({
                    modifier: modifier,
                    input: selectedModifierInput,
                    handleInputChangeCase: "textPosition" as InputCase,
                    inputPosition: modifierInputIndex,
                    width: "35",
                    key: "textPosition" + index + modifierInputIndex,
                    placeholder: "TEXT",
                  })
                );
              }
            }
            return elements;
          })()}
      </Flex>

      <Box bgColor={"ui.main"}>
        <CloseButton
          _hover={{ background: "gray.100", cursor: "pointer" }}
          onClick={() => {
            if (modifier.modifierId[0] !== null) {
              handleRemoveModifier(modifier.modifierId[0]);
            }
          }}
        />
      </Box>
    </Flex>
  ));

  const modifiersList = filteredModifiers.map((modifier) => (
    <Box
      key={modifier.modifierId[0]}
      p={2}
      _hover={{ background: "gray.100", cursor: "pointer" }}
      onClick={() => handleModifierSelect(modifier)}
    >
      {modifier.effect}
    </Box>
  ));

  return (
    <Flex direction="column" color="ui.dark" width={1200}>
      <Stack color={"ui.white"} mb={2}>
        {selectedModifiersList}
      </Stack>

      <Box bgColor={"ui.input"} color={"ui.white"} ref={ref} mr={8} ml={8}>
        <Input
          value={searchModifierText}
          onChange={(e) => handleInputChange(e.target.value, "modifier")}
          placeholder="+ Add modifier"
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
          onFocus={() => {
            if (!isExpanded) {
              toggleExpand();
            }
          }}
        />

        {isExpanded && (
          <Stack
            maxHeight="200px"
            overflowY="auto"
            bgColor={"ui.input"}
            onScroll={handleScroll}
          >
            {modifiersList}
          </Stack>
        )}
      </Box>
      {/* <Input
        placeholder="Enter a modifier"
        value={effectValueSearchInput}
        onChange={(e) => setEffectValueSearchInput(e.target.value)}
        width="200px"
        color={"ui.white"}
      /> */}

      {/* 
      <Menu>
        <MenuButton bgColor={"ui.white"} color={"ui.dark"}>
          Filter by Effect
        </MenuButton>
        <MenuList color={"ui.dark"} maxHeight="200px" overflowY="auto">
          {effects.map((effect, index) => (
            <MenuItem
              color={"ui.dark"}
              key={index}
              onClick={() => setEffectValueList(effect)}
            >
              {effect === effectValueList ? "✓" : ""} {effect}
            </MenuItem>
          ))}
        </MenuList>
      </Menu> */}
    </Flex>
  );
}

export default ModiferInput;
